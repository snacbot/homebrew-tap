cask "delve" do
  version "0.9.0"
  sha256 "b7df441e039ca91e255757634bb96b6df73bb0921031a74f92b12869c78e5bd4"

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
  depends_on macos: :tahoe

  app "Delve.app"

  zap trash: [
    "~/Library/Application Support/app.delve.Delve",
    "~/Library/Caches/app.delve.Delve",
    "~/Library/HTTPStorages/app.delve.Delve",
    "~/Library/Preferences/app.delve.Delve.plist",
    "~/Library/Saved Application State/app.delve.Delve.savedState",
  ]
end
