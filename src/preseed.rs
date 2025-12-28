use crate::schema::{Project, StorageLayout};
use std::fs;
use std::path::Path;

pub fn generate_preseed(project: &Project, output_dir: &Path) -> anyhow::Result<()> {
    let preseed_path = output_dir.join("preseed.cfg");

    let mut preseed = String::new();

    // Basic preseed settings
    preseed.push_str("# Preseed file for Debian installation\n");
    preseed.push_str("d-i debian-installer/locale string en_US.UTF-8\n");
    preseed.push_str("d-i keyboard-configuration/xkb-keymap select us\n");
    preseed.push_str("d-i netcfg/choose_interface select auto\n");
    preseed.push_str("d-i netcfg/get_hostname string workstation\n");
    preseed.push_str("d-i netcfg/get_domain string local\n");

    // Mirror settings
    preseed.push_str("d-i mirror/country string manual\n");
    preseed.push_str("d-i mirror/http/hostname string deb.debian.org\n");
    preseed.push_str("d-i mirror/http/directory string /debian\n");
    preseed.push_str("d-i mirror/suite string trixie\n");
    preseed.push_str("d-i mirror/http/proxy string\n");

    // Clock and timezone
    preseed.push_str("d-i clock-setup/utc boolean true\n");
    preseed.push_str("d-i time/zone string UTC\n");

    // Partitioning
    generate_partitioning(&project.storage_layout, &mut preseed);

    // User setup
    preseed.push_str("d-i passwd/root-password password root\n");
    preseed.push_str("d-i passwd/root-password-again password root\n");
    preseed.push_str("d-i passwd/user-fullname string Workstation User\n");
    preseed.push_str("d-i passwd/username string user\n");
    preseed.push_str("d-i passwd/user-password password password\n");
    preseed.push_str("d-i passwd/user-password-again password password\n");

    // Package selection
    preseed.push_str("tasksel tasksel/first multiselect standard, gnome-desktop\n");
    preseed.push_str("d-i pkgsel/include string nala\n");
    preseed.push_str("d-i pkgsel/upgrade select none\n");

    // Boot loader
    preseed.push_str("d-i grub-installer/only_debian boolean true\n");
    preseed.push_str("d-i grub-installer/with_other_os boolean false\n");

    // Finish installation
    preseed.push_str("d-i finish-install/reboot_in_progress note\n");

    // Late command for custom setup
    preseed.push_str("d-i preseed/late_command string \\\n");
    preseed.push_str("  in-target apt-get update; \\\n");
    preseed.push_str("  in-target apt-get install -y btrfs-progs; \\\n");
    preseed.push_str("  in-target mkdir -p /mnt/root_overlay; \\\n");
    preseed.push_str("  in-target mount -t overlay overlay -o lowerdir=/,upperdir=/mnt/root_overlay/upper,workdir=/mnt/root_overlay/work /; \\\n");
    preseed.push_str("  in-target echo 'overlay / overlay ro 0 0' >> /etc/fstab; \\\n");
    preseed.push_str("  in-target systemctl enable systemd-readahead-collect.service; \\\n");
    preseed.push_str("  in-target systemctl enable systemd-readahead-replay.service\n");

    fs::write(&preseed_path, preseed)?;
    println!("✅ Preseed generated at: {:?}", preseed_path);
    Ok(())
}

fn generate_partitioning(_layout: &StorageLayout, preseed: &mut String) {
    preseed.push_str("d-i partman-auto/disk string /dev/sda\n");
    preseed.push_str("d-i partman-auto/method string crypto\n");
    preseed.push_str("d-i partman-lvm/device_remove_lvm boolean true\n");
    preseed.push_str("d-i partman-md/device_remove_md boolean true\n");
    preseed.push_str("d-i partman-auto/choose_recipe select custom\n");

    // Custom recipe for EFI, ext4 boot, LUKS BTRFS
    preseed.push_str("d-i partman-auto/expert_recipe string \\\n");
    preseed.push_str("  custom :: \\\n");
    preseed.push_str("    512 512 512 fat32 \\\n");
    preseed.push_str("      $primary{ } $bootable{ } \\\n");
    preseed.push_str("      method{ efi } format{ } \\\n");
    preseed.push_str("    . \\\n");
    preseed.push_str("    100000 100000 100000 ext4 \\\n");
    preseed.push_str("      $primary{ } \\\n");
    preseed.push_str("      method{ format } format{ } \\\n");
    preseed.push_str("      use_filesystem{ } filesystem{ ext4 } \\\n");
    preseed.push_str("      mountpoint{ /boot } \\\n");
    preseed.push_str("    . \\\n");
    preseed.push_str("    100000 100000 100000 btrfs \\\n");
    preseed.push_str("      $primary{ } \\\n");
    preseed.push_str("      method{ format } format{ } \\\n");
    preseed.push_str("      use_filesystem{ } filesystem{ btrfs } \\\n");
    preseed.push_str("      mountpoint{ / } \\\n");
    preseed.push_str("      options{ compress=zstd } \\\n");
    preseed.push_str("    . \\\n");
    preseed.push_str("    500000 500000 500000 btrfs \\\n");
    preseed.push_str("      $primary{ } \\\n");
    preseed.push_str("      method{ format } format{ } \\\n");
    preseed.push_str("      use_filesystem{ } filesystem{ btrfs } \\\n");
    preseed.push_str("      mountpoint{ /home } \\\n");
    preseed.push_str("      options{ compress=zstd } \\\n");
    preseed.push_str("    . \\\n");
    preseed.push_str("    64000 64000 64000 linux-swap \\\n");
    preseed.push_str("      $primary{ } \\\n");
    preseed.push_str("      method{ swap } format{ } \\\n");
    preseed.push_str("    .\n");

    preseed.push_str("d-i partman-auto/confirm boolean true\n");
    preseed.push_str("d-i partman-crypto/passphrase password passphrase\n");
    preseed.push_str("d-i partman-crypto/passphrase-again password passphrase\n");
}