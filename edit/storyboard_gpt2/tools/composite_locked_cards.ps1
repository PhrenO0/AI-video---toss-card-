[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$BaseCommit = "07df225cd2beff67a9ba3c609900a79ba7d47a0e",
    [string]$CalibrationDir,
    [switch]$CalibrationOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\..\.."))
$assetPath = Join-Path $repoRoot "assets\toss-card\pre-card-hologram-front (1).png"
$expectedAssetSha256 = "52294CAEE8999C38D5B0E0FB27517F0CFF18655083A4C395B7B4E3668BEF1FDA"

# The generated people, hands, gates and lighting come from commit 07df225.
# Only the bounded card surfaces below are replaced. Destination geometry uses
# System.Drawing's three-point affine mapping: upper-left, upper-right,
# lower-left. The fourth corner is inferred, so source pixels remain exact
# apart from deterministic interpolation/downsampling.
$shots = @(
    [pscustomobject]@{
        Id = "S02"
        RelativePath = "edit/storyboard_gpt2/frames/raw/S02.png"
        BaseSha256 = "9A13C153311B62C613C7742C268BE93EEA12E3DDEF64EA4F970416AAF2D2A62C"
        Mode = "Neutral"
        Points = @(
            [System.Drawing.PointF]::new(448.0, 875.0),
            [System.Drawing.PointF]::new(489.0, 879.0),
            [System.Drawing.PointF]::new(446.0, 895.0)
        )
        Occlusion = ,([System.Drawing.PointF[]]@(
                [System.Drawing.PointF]::new(441.0, 883.0),
                [System.Drawing.PointF]::new(460.0, 884.0),
                [System.Drawing.PointF]::new(465.0, 901.0),
                [System.Drawing.PointF]::new(447.0, 905.0),
                [System.Drawing.PointF]::new(440.0, 895.0)
            ))
        Crop = [System.Drawing.Rectangle]::new(380, 790, 180, 180)
    },
    [pscustomobject]@{
        Id = "S12"
        RelativePath = "edit/storyboard_gpt2/frames/raw/S12.png"
        BaseSha256 = "194DCC0408D725D0C87A3237B31A8581D975029921908E38969F0EC4F2606E4B"
        Mode = "Official"
        Points = @(
            [System.Drawing.PointF]::new(220.0, 767.0),
            [System.Drawing.PointF]::new(304.0, 781.0),
            [System.Drawing.PointF]::new(237.0, 862.0)
        )
        Occlusion = ,([System.Drawing.PointF[]]@(
                [System.Drawing.PointF]::new(265.0, 748.0),
                [System.Drawing.PointF]::new(313.0, 752.0),
                [System.Drawing.PointF]::new(315.0, 794.0),
                [System.Drawing.PointF]::new(279.0, 796.0),
                [System.Drawing.PointF]::new(264.0, 779.0)
            ))
        Crop = [System.Drawing.Rectangle]::new(160, 700, 220, 240)
    },
    [pscustomobject]@{
        Id = "S13"
        RelativePath = "edit/storyboard_gpt2/frames/raw/S13.png"
        BaseSha256 = "11B359F68E97E5E97DBFC4CACF023D5C8DE4632229B4080158AC54174D78B770"
        Mode = "Official"
        Points = @(
            [System.Drawing.PointF]::new(575.0, 899.0),
            [System.Drawing.PointF]::new(615.0, 903.0),
            [System.Drawing.PointF]::new(578.0, 947.0)
        )
        Occlusion = ,([System.Drawing.PointF[]]@(
                [System.Drawing.PointF]::new(594.0, 886.0),
                [System.Drawing.PointF]::new(619.0, 891.0),
                [System.Drawing.PointF]::new(619.0, 917.0),
                [System.Drawing.PointF]::new(600.0, 919.0),
                [System.Drawing.PointF]::new(593.0, 903.0)
            ))
        Crop = [System.Drawing.Rectangle]::new(520, 840, 150, 170)
    }
)

function Export-GitBlob {
    param(
        [Parameter(Mandatory)][string]$Revision,
        [Parameter(Mandatory)][string]$RelativePath,
        [Parameter(Mandatory)][string]$Destination
    )

    $spec = "${Revision}:$($RelativePath.Replace('\', '/'))"
    $process = Start-Process -FilePath "git" `
        -WorkingDirectory $repoRoot `
        -ArgumentList @("cat-file", "blob", $spec) `
        -RedirectStandardOutput $Destination `
        -NoNewWindow -Wait -PassThru
    if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $Destination)) {
        throw "Could not export $spec"
    }
}

function New-NeutralCardTexture {
    $texture = [System.Drawing.Bitmap]::new(650, 1024, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($texture)
    try {
        $graphics.Clear([System.Drawing.Color]::FromArgb(255, 62, 66, 70))
        $edgePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(255, 86, 91, 96), 9.0)
        try {
            $graphics.DrawRectangle($edgePen, 8, 8, 633, 1007)
        }
        finally {
            $edgePen.Dispose()
        }
    }
    finally {
        $graphics.Dispose()
    }
    return $texture
}

function Save-CalibrationCrop {
    param(
        [Parameter(Mandatory)][System.Drawing.Bitmap]$Bitmap,
        [Parameter(Mandatory)][System.Drawing.Rectangle]$Crop,
        [Parameter(Mandatory)][string]$Path
    )

    $scale = 4
    $preview = [System.Drawing.Bitmap]::new($Crop.Width * $scale, $Crop.Height * $scale)
    $graphics = [System.Drawing.Graphics]::FromImage($preview)
    try {
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
        $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
        $graphics.DrawImage($Bitmap, [System.Drawing.Rectangle]::new(0, 0, $preview.Width, $preview.Height), $Crop, [System.Drawing.GraphicsUnit]::Pixel)

        $gridPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(150, 255, 40, 40), 1.0)
        $font = [System.Drawing.Font]::new("Consolas", 10.0, [System.Drawing.FontStyle]::Bold)
        $brush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::Yellow)
        try {
            for ($x = 0; $x -le $Crop.Width; $x += 10) {
                $px = $x * $scale
                $graphics.DrawLine($gridPen, $px, 0, $px, $preview.Height)
                if (($x % 20) -eq 0) { $graphics.DrawString(($Crop.X + $x), $font, $brush, $px + 2, 2) }
            }
            for ($y = 0; $y -le $Crop.Height; $y += 10) {
                $py = $y * $scale
                $graphics.DrawLine($gridPen, 0, $py, $preview.Width, $py)
                if (($y % 20) -eq 0) { $graphics.DrawString(($Crop.Y + $y), $font, $brush, 2, $py + 2) }
            }
        }
        finally {
            $gridPen.Dispose()
            $font.Dispose()
            $brush.Dispose()
        }
        $preview.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $graphics.Dispose()
        $preview.Dispose()
    }
}

function Test-SkinPixel {
    param([Parameter(Mandatory)][System.Drawing.Color]$Color)

    $r = [int]$Color.R
    $g = [int]$Color.G
    $b = [int]$Color.B
    return ($r -ge 105 -and $g -ge 55 -and $b -ge 35 -and
        $r -ge ($g + 9) -and $r -ge ($b + 16) -and
        ([Math]::Max($r, [Math]::Max($g, $b)) - [Math]::Min($r, [Math]::Min($g, $b))) -ge 18)
}

function Restore-SkinOcclusion {
    param(
        [Parameter(Mandatory)][System.Drawing.Bitmap]$Base,
        [Parameter(Mandatory)][System.Drawing.Bitmap]$Output,
        [Parameter(Mandatory)][System.Drawing.PointF[]]$Polygon
    )

    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    try {
        $path.AddPolygon($Polygon)
        $bounds = $path.GetBounds()
        $minX = [Math]::Max(0, [int][Math]::Floor($bounds.Left))
        $maxX = [Math]::Min($Base.Width - 1, [int][Math]::Ceiling($bounds.Right))
        $minY = [Math]::Max(0, [int][Math]::Floor($bounds.Top))
        $maxY = [Math]::Min($Base.Height - 1, [int][Math]::Ceiling($bounds.Bottom))

        for ($y = $minY; $y -le $maxY; $y++) {
            for ($x = $minX; $x -le $maxX; $x++) {
                if (-not $path.IsVisible($x + 0.5, $y + 0.5)) { continue }
                $basePixel = $Base.GetPixel($x, $y)
                if (Test-SkinPixel -Color $basePixel) {
                    $Output.SetPixel($x, $y, $basePixel)
                }
            }
        }
    }
    finally {
        $path.Dispose()
    }
}

if (-not (Test-Path -LiteralPath $assetPath)) {
    throw "Official card asset not found: $assetPath"
}
$actualAssetSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $assetPath).Hash
if ($actualAssetSha256 -ne $expectedAssetSha256) {
    throw "Official card asset SHA-256 mismatch. Expected $expectedAssetSha256; got $actualAssetSha256."
}

if ($CalibrationDir) {
    $CalibrationDir = [System.IO.Path]::GetFullPath($CalibrationDir)
    [System.IO.Directory]::CreateDirectory($CalibrationDir) | Out-Null
}

$official = [System.Drawing.Bitmap]::FromFile($assetPath)
$neutral = New-NeutralCardTexture
try {
    foreach ($shot in $shots) {
        $tempBase = [System.IO.Path]::GetTempFileName()
        try {
            Export-GitBlob -Revision $BaseCommit -RelativePath $shot.RelativePath -Destination $tempBase
            $actualBaseSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $tempBase).Hash
            if ($actualBaseSha256 -ne $shot.BaseSha256) {
                throw "Base blob SHA-256 mismatch for $($shot.Id). Expected $($shot.BaseSha256); got $actualBaseSha256."
            }
            $base = [System.Drawing.Bitmap]::FromFile($tempBase)
            try {
                if ($CalibrationDir) {
                    Save-CalibrationCrop -Bitmap $base -Crop $shot.Crop -Path (Join-Path $CalibrationDir "$($shot.Id)-base-grid.png")
                }
                if ($CalibrationOnly) { continue }

                $output = [System.Drawing.Bitmap]::new($base.Width, $base.Height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
                $graphics = [System.Drawing.Graphics]::FromImage($output)
                try {
                    $graphics.DrawImageUnscaled($base, 0, 0)
                    $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceOver
                    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
                    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
                    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
                    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

                    $texture = if ($shot.Mode -eq "Official") { $official } else { $neutral }
                    $graphics.DrawImage($texture, [System.Drawing.PointF[]]$shot.Points)

                }
                finally {
                    $graphics.Dispose()
                }

                foreach ($polygon in $shot.Occlusion) {
                    Restore-SkinOcclusion -Base $base -Output $output -Polygon ([System.Drawing.PointF[]]$polygon)
                }

                $destination = Join-Path $repoRoot $shot.RelativePath
                if ($PSCmdlet.ShouldProcess($destination, "Composite locked card surface from $BaseCommit")) {
                    $output.Save($destination, [System.Drawing.Imaging.ImageFormat]::Png)
                }
                if ($CalibrationDir) {
                    Save-CalibrationCrop -Bitmap $output -Crop $shot.Crop -Path (Join-Path $CalibrationDir "$($shot.Id)-composite-grid.png")
                }
                $output.Dispose()
            }
            finally {
                $base.Dispose()
            }
        }
        finally {
            Remove-Item -LiteralPath $tempBase -Force -ErrorAction SilentlyContinue
        }
    }
}
finally {
    $official.Dispose()
    $neutral.Dispose()
}
