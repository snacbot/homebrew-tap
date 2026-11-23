cask "delve" do
  version "0.14.4"
  sha256 "917fb06bc40a3abea09073ef129c040a104526a6ab066c9222540b8634ef87a6"

  url "https://github.com/snacbot/delve-releases/releases/download/v#{version}/Delve-#{version}.dmg"
  name "Delve"
  desc "Disk space analyzer with a GPU-rendered treemap"
  homepage "https://khaosstudio.com/delve/"

  # Delve ships its own Sparkle updates from the same feed the app reads.
  livecheck do
    url "https://raw.githubusercontent.com/snacbot/delve-releases/main/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :monterey

  app "Delve.app"

  zap trash: [
    "~/Library/Application Support/app.delve.Delve",
    "~/Library/Caches/app.delve.Delve",
    "~/Library/HTTPStorages/app.delve.Delve",
    "~/Library/Preferences/app.delve.Delve.plist",
    "~/Library/Saved Application State/app.delve.Delve.savedState",
  ]
end
