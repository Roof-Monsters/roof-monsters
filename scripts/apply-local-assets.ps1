$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$utf8 = New-Object System.Text.UTF8Encoding $false

$replacements = [ordered]@{
  'https://roofmonsters.co/wp-content/uploads/2025/01/unnamed.png' = 'assets/images/brand/logo.png'
  'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_6006.jpg' = 'assets/images/gallery/installation-01.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_5993.jpg' = 'assets/images/gallery/project-02.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_5994-1.jpg' = 'assets/images/gallery/completed-03.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/IMG_6015.jpg' = 'assets/images/gallery/installation-04.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/473619572_122153237438329090_1935536644784443363_n.jpg' = 'assets/images/team/crew-01.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/436379617_122100952934329090_785895433237978047_n-1536x1536.jpg' = 'assets/images/team/rob-lewis.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/436379617_122100952934329090_785895433237978047_n-1024x1024.jpg' = 'assets/images/team/rob-lewis-square.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/FireShot-Capture-102-Atlas-roof-pictures-Google-Drive-drive.google.com_-e1737566288472.png' = 'assets/images/gallery/atlas-install-01.png'
  'https://roofmonsters.co/wp-content/uploads/2025/01/FireShot-Capture-103-Atlas-roof-pictures-Google-Drive-drive.google.com_-e1737566357418.png' = 'assets/images/gallery/atlas-install-02.png'
  'https://roofmonsters.co/wp-content/uploads/2025/01/Atlas_Designer_Shingles_featuring_Scotchgard_-_Lock-up_2-1024x400.jpg' = 'assets/images/brand/atlas-shingles-banner.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/New-Roof-Pinellas-County-Florida.jpg' = 'assets/images/gallery/pinellas-new-roof.jpg'
  'https://roofmonsters.co/wp-content/uploads/2024/03/F6.jpg' = 'assets/images/backgrounds/stats-section.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/01/us-veteran-woman-leaving-for-military-service--1536x1024.jpg' = 'assets/images/offers/military-discount-hero.jpg'
  'https://roofmonsters.co/wp-content/uploads/2024/05/roof-instalaltion.webp' = 'assets/images/services/inspections.webp'
  'https://roofmonsters.co/wp-content/uploads/2024/05/roof-instalation-roofmonster-878x1536.webp' = 'assets/images/services/installation.webp'
  'https://roofmonsters.co/wp-content/uploads/2024/05/repair-maintenance-878x1536.webp' = 'assets/images/services/repairs.webp'
  'https://roofmonsters.co/wp-content/uploads/2024/05/guteere2-878x1536.webp' = 'assets/images/services/gutters.webp'
  'https://roofmonsters.co/wp-content/uploads/2024/05/emergency-roof-repair-878x1536.webp' = 'assets/images/services/storm-damage.webp'
  'https://roofmonsters.co/wp-content/uploads/2024/03/F5.jpg' = 'assets/images/gallery/completed-05.jpg'
  'https://roofmonsters.co/wp-content/uploads/2024/05/F25.jpg' = 'assets/images/team/crew-at-work.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7565.jpeg' = 'assets/images/gallery/completed-06.jpeg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7610.jpeg' = 'assets/images/gallery/installation-07.jpeg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7611.jpg' = 'assets/images/gallery/replacement-08.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/IMG_7612.jpg' = 'assets/images/gallery/project-09.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/4353A7A7F8612BEFC428715EDFA7CC95-scaled.jpg' = 'assets/images/gallery/quality-work.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/08/F28F4EF9BB3B4DDEE1861426C663ACB0-scaled.jpg' = 'assets/images/gallery/tampa-bay-project.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/10/Gemini_Generated_Image_5fh1575fh1575fh1.png' = 'assets/images/blog/october-roofing-season.png'
  'https://roofmonsters.co/wp-content/uploads/2025/04/aftermath-of-hurricane-debby-flooding-natural-disaster-.jpg' = 'assets/images/blog/hurricane-prep.jpg'
  'https://roofmonsters.co/wp-content/uploads/2025/04/happy-customer.jpg' = 'assets/images/blog/happy-customer.jpg'
}

$files = Get-ChildItem $root -Recurse -Include *.html,*.css |
  Where-Object { $_.Name -notmatch 'GROWTH-ROADMAP' }

foreach ($file in $files) {
  $content = [System.IO.File]::ReadAllText($file.FullName)

  foreach ($key in $replacements.Keys) {
    $content = $content.Replace($key, $replacements[$key])
  }

  # Testimonial/review avatars should not use the logo
  $content = [regex]::Replace($content, '(?s)(class="(?:testimonial-header|review-header)">\s*<img src=")assets/images/brand/logo\.png"', '${1}assets/images/brand/default-avatar.svg"')

  # Hero slide backgrounds
  $content = $content.Replace('class="hero-slide-bg ken-burns" style="background-image: url(''assets/images/gallery/atlas-install-01.png'');"', 'class="hero-slide-bg ken-burns bg-hero-slide-1"')
  $content = $content.Replace('class="hero-slide-bg ken-burns" style="background-image: url(''assets/images/gallery/installation-04.jpg'');"', 'class="hero-slide-bg ken-burns bg-hero-slide-2"')
  $content = $content.Replace('class="hero-slide-bg ken-burns" style="background-image: url(''assets/images/gallery/installation-01.jpg'');"', 'class="hero-slide-bg ken-burns bg-hero-slide-3"')

  # Section backgrounds
  $content = $content.Replace('class="company-section section-pad" style="background-image: url(''assets/images/backgrounds/stats-section.jpg''); background-size: cover; background-position: center; position: relative;" data-stats-section', 'class="company-section section-pad bg-stats-section" data-stats-section')
  $content = $content.Replace('class="offers-section" style="background-image: url(''assets/images/offers/military-discount-hero.jpg'');"', 'class="offers-section bg-offers-military"')
  $content = $content.Replace('class="atlas-banner" style="background-image: url(''assets/images/gallery/installation-04.jpg'');"', 'class="atlas-banner bg-atlas-banner-roof"')
  $content = $content.Replace('class="atlas-banner" style="background-image: url(''assets/images/brand/atlas-shingles-banner.jpg'');"', 'class="atlas-banner bg-atlas-banner-shingles"')

  # Section background utility classes
  $content = [regex]::Replace($content, 'class="([^"]*)" style="background:var\(--bg-light\);"', 'class="$1 section-bg-light"')
  $content = [regex]::Replace($content, 'class="([^"]*)" style="background:var\(--bg\);"', 'class="$1 section-bg-white"')
  $content = $content.Replace('style="width:100%; border-radius:12px; box-shadow:0 8px 40px rgba(0,0,0,0.12); display:block; margin-bottom:20px;"', 'class="about-photo about-photo--spaced"')
  $content = $content.Replace('style="width:100%; border-radius:12px; box-shadow:0 8px 40px rgba(0,0,0,0.12); display:block;"', 'class="about-photo"')
  $content = $content.Replace('style="margin-top:20px;"', 'class="u-mt-20"')

  # Remove page-local style blocks
  $content = [regex]::Replace($content, '(?s)\s*<style>.*?</style>\s*', "`n", 1)

  [System.IO.File]::WriteAllText($file.FullName, $content, $utf8)
  Write-Host "Updated: $($file.Name)"
}

$skylightsPath = Join-Path $root 'service-skylights.html'
if (Test-Path $skylightsPath) {
  $sk = [System.IO.File]::ReadAllText($skylightsPath)
  $sk = $sk.Replace('assets/images/services/repairs.webp', 'assets/images/services/skylights.webp')
  [System.IO.File]::WriteAllText($skylightsPath, $sk, $utf8)
  Write-Host 'Updated: service-skylights.html (skylights image path)'
}

$remaining = Get-ChildItem $root -Recurse -Include *.html,*.css |
  Where-Object { $_.Name -notmatch 'GROWTH-ROADMAP' } |
  ForEach-Object { Select-String -Path $_.FullName -Pattern 'wp-content' -SimpleMatch } |
  Where-Object { $_ }
if ($remaining) {
  Write-Host "WARNING: wp-content refs remain:"
  $remaining | ForEach-Object { $_.Line.Trim() }
} else {
  Write-Host 'All wp-content references removed.'
}
