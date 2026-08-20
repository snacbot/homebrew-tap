cask "delve" do
  version "0.8.13"
  sha256 "3c189717de1d0a1987f29d5105e48829c392a197eacf9935a593a6b2f06f401a"

  url "https://github.com/snacbot/delve-releases/releases/download/v#{version}/Delve-#{version}.dmg",
      verified: "github.com/snacbot/delve-releases/"
  name "Delve"
  desc "Disk space analyzer with a GPU-rendered treemap"
  homepage "https://khaosstudio.com/delve/"

  # Delve ships its own Sparkle updates from the same feed the app reads.
  livecheck do
    url "https://raw.githubusercontent.com/snacbot/delve-releases/main/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on macos: :tahoe
  depends_on arch: :arm64

  app "Delve.app"

  zap trash: [
    "~/Library/Application Support/app.delve.Delve",
    "~/Library/Caches/app.delve.Delve",
    "~/Library/HTTPStorages/app.delve.Delve",
    "~/Library/Preferences/app.delve.Delve.plist",
    "~/Library/Saved Application State/app.delve.Delve.savedState",
  ]
end
