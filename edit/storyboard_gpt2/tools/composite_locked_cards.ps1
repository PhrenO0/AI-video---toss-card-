[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$BaseCommit = "07df225",
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
        Mode = "Neutral"
        Points = @(
            [System.Drawing.PointF]::new(449.0, 877.0),
            [System.Drawing.PointF]::new(481.0, 882.0),
            [System.Drawing.PointF]::new(447.0, 894.0)
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
        Mode = "Official"
        Points = @(
            [System.Drawing.PointF]::new(223.0, 771.0),
            [System.Drawing.PointF]::new(287.0, 781.0),
            [System.Drawing.PointF]::new(239.0, 850.0)
        )
        Occlusion = ,([System.Drawing.PointF[]]@(
                [System.Drawing.PointF]::new(270.0, 760.0),
                [System.Drawing.PointF]::new(292.0, 769.0),
                [System.Drawing.PointF]::new(294.0, 789.0),
                [System.Drawing.PointF]::new(279.0, 789.0),
                [System.Drawing.PointF]::new(268.0, 778.0)
            ))
        Crop = [System.Drawing.Rectangle]::new(160, 700, 220, 240)
    },
    [pscustomobject]@{
        Id = "S13"
        RelativePath = "edit/storyboard_gpt2/frames/raw/S13.png"
        Mode = "Official"
        Points = @(
            [System.Drawing.PointF]::new(578.0, 901.0),
            [System.Drawing.PointF]::new(608.0, 903.0),
            [System.Drawing.PointF]::new(580.0, 943.0)
        )
        Occlusion = ,([System.Drawing.PointF[]]@(
                [System.Drawing.PointF]::new(599.0, 889.0),
                [System.Drawing.PointF]::new(614.0, 895.0),
                [System.Drawing.PointF]::new(612.0, 913.0),
                [System.Drawing.PointF]::new(601.0, 916.0),
                [System.Drawing.PointF]::new(596.0, 903.0)
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

                    foreach ($polygon in $shot.Occlusion) {
                        $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
                        try {
                            $path.AddPolygon([System.Drawing.PointF[]]$polygon)
                            $graphics.SetClip($path)
                            $graphics.DrawImageUnscaled($base, 0, 0)
                            $graphics.ResetClip()
                        }
                        finally {
                            $path.Dispose()
                        }
                    }
                }
                finally {
                    $graphics.Dispose()
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
