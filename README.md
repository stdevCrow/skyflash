# skyflash is a tool to configure & flash skybian base images for the official skycoin skyminers

With this tool you will be able configure the default [skybian](https://github.com/simelo/skybian) image to your custom environment and create the needed images for it.

The resulting images will only run on the official skyminer hardware, aka: Orange Pi Prime SBC.

The tool has two variants:

* A general use GUI tool (skyflash) that works on Linux/Mac/Windows
* A Linux only CLI tool (skyflash-cli) **_for developers and advanced users_**.

## Skyflash GUI tool

The preferred method to configure & flash skybian images is by using this GUI tool

### Installing

To install this tool, go to the [Releases](https://github.com/skycoin/skyflash/releases) link on this page and grab the file corresponding file to your OS, use the following table to figure it out:

| Operating System | You must download the one... |
|:----------------:|:--------------------------------:|
| Windows | ...that ends with **.exe** |
| Linux | ...that ends with **.deb** |
| MacOS | ...that ends with **.dmg** |

Installing it and running is done by the default OS way.

### Usage

To see more detailed instructions on how to use the Skyflash GUI utility please visit the [User's Manual](USER_MANUAL.md)

## skyflash-cli tool

The tool `skyflash-cli` is intended to be run on linux (soon on Mac too) and will generate the needed images for a base image.

Once you has created your images you will need to use a tool to burn these images to the uSD cards, we recommend [BalenaEtcher](https://www.balena.io/etcher/) a cross OS tool.

### Step 1: Download the default skybian image

Go to [skybian](https://github.com/skycoin/skybian) releases and download the latest image, decompress it and put the base image on the folder where `skyflash-cli` resides; or copy the `skyflash-cli` tool to the folder where you have the skybian image.

### Step 2: Run the tool

`skyflash-cli` has a few options that you can see if you run it without arguments (`skyflash-cli`) or with '-h' switch (`skyflash-cli -h`)

For a default configuration of skybian as a skyminer you just need to run it like this:

```sh
./skyflash-cli -a Skybian-0.1.0.img
```

This will generate 8 images, one for the manager and 7 minions. Network configuration is the skyminers default:

* Network: 192.168.0.0/24
* Netmask: 255.255.255.0 (aka: /24)
* Gateway: 192.168.0.1
* DNS servers: 1.0.0.1, 1.1.1.1
* Manager IP: 192.168.0.2
* Minions IPs: 192.168.0.[3-9] (7 minions)

If you need a different setup just check the `skyflash-cli -h` to know more, for example for a manager and 22 minions with this details:

* Network: 172.16.22.0/24
* Gateway: 172.16.22.1
* DNS servers: 172.16.22.1, 1.1.1.1
* Manager: 172.16.22.10
* Minions: 172.16.22.100 to 172.16.22.121

**Tip:** If you don't care about the minions IP being contiguous you can declare a range that is greater than the minions count and the script will allocate the IPs in a scattered way inside the range you stated.

```sh
./skyflash-cli -g 172.16.22.1 -d "172.16.22.1, 1.1.1.1" -m 172.16.22.10 -n 100-121 -i Skybian-0.1.0.img
```

Please note that in the case of the DNS (option '-d') if you need to pass more than one IP you need to surround it with double quotes and separate it with a comma and a space, just like the example above.

### Releases

To do a release you must follow these steps:

0. Check if there are commits on the master branch that must be applied to develop (hot fixes or security ones), apply them and fix any merge issues.
0. On develop branch, check any pending issues in order to close them if possible on this release and close them is possible.
0. Check the latest release of Skybian and if the URL of the latest image is different rise a issue and solve it by the default way.
0. Merge the develop branch into the release one and fix any conflicts if any.
0. Update the new version number in the `setup.py` & `skyflash/data/skyflash.qml` files.
0. Update the `CHANGELOG.md` file with any needed info and move the `Unreleased` part to the new release version.
0. Review & update the `README.md` file for any needed updates or changes that need attention in the front page.
0. Wait for travis to validate all the changes.
0. On success, check the draft release is published on the repository, improve it and keep it as a draft.
0. Download the releases files and test them.
0. If problems are found with raise issues where needed (skyflash/skybian) and fix them before continue with the next step.
0. Download the releases files after the fix in the previous step (if needed) and test them.
0. Fix any issues if found (work in the release branch)
0. After all problems are solved and work as expected, tag it as `Skyflash-X.Y.Z` & raise a PR against master branch, solve any issues and merge it.
0. Wait for travis completion and check the release files are published on the Github repository under releases.
0. Edit & comment the release with the changes in CHANGELOG.md that match this release, change status from Draft to Official release.
0. Merge master into develop.
0. Check if there is needed to raise issues & PR on the following repositories:

    * [Skybian](https://github.com/skycoin/skybian): if needed.
    * [Skycoin](https://github.com/skycoin/skycoin): mentions in it's README.md and elsewhere if applicable
    * [Skywire](https://github.com/skycoin/skywire): to note the new release and the use of skybian/skyflash