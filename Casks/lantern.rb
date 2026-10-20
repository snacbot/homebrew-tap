cask "lantern" do
  version "0.2.0"
  sha256 "61767e38c6df66205a7cf5fdf87f69247a51f5592f9d92bff7d48f126a2226ab"

  url "https://github.com/snacbot/lantern-releases/releases/download/mac-v#{version}/Lantern-#{version}.dmg"
  name "Lantern"
  desc "Control monitor brightness across computers on your local network"
  homepage "https://khaosstudio.com/lantern/"

  livecheck do
    url "https://raw.githubusercontent.com/snacbot/lantern-releases/main/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on macos: :ventura

  app "Lantern.app"

  zap trash: [
    "~/Library/Application Support/LightSync",
    "~/Library/Caches/com.lightsync.app",
    "~/Library/HTTPStorages/com.lightsync.app",
    "~/Library/Preferences/com.lightsync.app.plist",
    "~/Library/Saved Application State/com.lightsync.app.savedState",
  ]
end
