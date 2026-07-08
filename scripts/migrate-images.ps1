$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent

$downloads = @(
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/unnamed.png'; Path = 'assets/images/brand/logo.png' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_6006.jpg'; Path = 'assets/images/gallery/installation-01.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_5993.jpg'; Path = 'assets/images/gallery/project-02.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_5994-1.jpg'; Path = 'assets/images/gallery/completed-03.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_6015.jpg'; Path = 'assets/images/gallery/installation-04.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/473619572_122153237438329090_1935536644784443363_n.jpg'; Path = 'assets/images/team/crew-01.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/436379617_122100952934329090_785895433237978047_n-1536x1536.jpg'; Path = 'assets/images/team/rob-lewis.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/436379617_122100952934329090_785895433237978047_n-1024x1024.jpg'; Path = 'assets/images/team/rob-lewis-square.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/FireShot-Capture-102-Atlas-roof-pictures-Google-Drive-drive.google.com_-e1737566288472.png'; Path = 'assets/images/gallery/atlas-install-01.png' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/FireShot-Capture-103-Atlas-roof-pictures-Google-Drive-drive.google.com_-e1737566357418.png'; Path = 'assets/images/gallery/atlas-install-02.png' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/Atlas_Designer_Shingles_featuring_Scotchgard_-_Lock-up_2-1024x400.jpg'; Path = 'assets/images/brand/atlas-shingles-banner.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/New-Roof-Pinellas-County-Florida.jpg'; Path = 'assets/images/gallery/pinellas-new-roof.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/03/F6.jpg'; Path = 'assets/images/backgrounds/stats-section.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/01/us-veteran-woman-leaving-for-military-service--1536x1024.jpg'; Path = 'assets/images/offers/military-discount-hero.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/05/roof-instalaltion.webp'; Path = 'assets/images/services/inspections.webp' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/05/roof-instalation-roofmonster-878x1536.webp'; Path = 'assets/images/services/installation.webp' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/05/repair-maintenance-878x1536.webp'; Path = 'assets/images/services/repairs.webp' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/05/guteere2-878x1536.webp'; Path = 'assets/images/services/gutters.webp' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/05/emergency-roof-repair-878x1536.webp'; Path = 'assets/images/services/storm-damage.webp' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/03/F5.jpg'; Path = 'assets/images/gallery/completed-05.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2024/05/F25.jpg'; Path = 'assets/images/team/crew-at-work.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7565.jpeg'; Path = 'assets/images/gallery/completed-06.jpeg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7610.jpeg'; Path = 'assets/images/gallery/installation-07.jpeg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7611.jpg'; Path = 'assets/images/gallery/replacement-08.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7612.jpg'; Path = 'assets/images/gallery/project-09.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/4353A7A7F8612BEFC428715EDFA7CC95-scaled.jpg'; Path = 'assets/images/gallery/quality-work.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/08/F28F4EF9BB3B4DDEE1861426C663ACB0-scaled.jpg'; Path = 'assets/images/gallery/tampa-bay-project.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/10/Gemini_Generated_Image_5fh1575fh1575fh1.png'; Path = 'assets/images/blog/october-roofing-season.png' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/04/aftermath-of-hurricane-debby-flooding-natural-disaster-.jpg'; Path = 'assets/images/blog/hurricane-prep.jpg' }
  @{ Url = 'https://roofmonsters.co/wp-content/uploads/2025/04/happy-customer.jpg'; Path = 'assets/images/blog/happy-customer.jpg' }
)

foreach ($item in $downloads) {
  $dest = Join-Path $root $item.Path
  $dir = Split-Path $dest -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  if (Test-Path $dest) {
    Write-Host "Skip (exists): $($item.Path)"
    continue
  }
  Write-Host "Downloading: $($item.Path)"
  Invoke-WebRequest -Uri $item.Url -OutFile $dest -UseBasicParsing
}

# Skylights page reuses repair photo
$skylights = Join-Path $root 'assets/images/services/skylights.webp'
$repairs = Join-Path $root 'assets/images/services/repairs.webp'
if ((Test-Path $repairs) -and -not (Test-Path $skylights)) {
  Copy-Item $repairs $skylights
  Write-Host 'Copied repairs.webp -> skylights.webp'
}

Write-Host 'Done. Downloaded' $downloads.Count 'assets (+ skylights copy if needed).'
