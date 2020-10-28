# CredHelper

Swapping out AWS credentials every day on multiple workspaces is very time consuming, tedious, and not the best use of your time.

Introducing, `credhelper`! This simple python utility lets you quickly and easily update all your AWS credentials in all of your TFC workspaces within a list of given organizations.

## Getting Started

This little app is pretty simple to setup. There are a few configurable options, which I'll cover directly.

### Requirements

* Python 3
* pip for Python 3

### Configuration

From the command line:

* Clone this repository
* Change into the `credhelper` directory
* run `pip install -r requirements.txt`
* Rename `config.ini.example` to `config.ini`
* Edit the `config.ini` file and enter your values
  - `TerraformToken`: Your Terraform API token. Should be your user API token to ensure you have access to all of your own workspaces.
  - `Organizations`: The organizations you're wanting to run this script against, it is a comma seperated list.
  - `AwsAccessKeyNames`: List of variable names representing the AWS Access Key
  - `AwsSecretKeyNames`: List of variable names representing the AWS Secret Key ID
  - `AwsSessionTokenNames`: List of variable names representing the AWS Session Token

The variable names can be either environment variables or terraform variables.

## Using the App

* Login to **Doormat** (internal HashiCorp application)
* Locate the account you'd like credentials for, and under the **CLI** column, click the **key** icon
  ![CLI Credentials](https://github.com/kevincloud/credhelper/blob/master/docs/images/cli-button.png)
* Click the copy button in the first option, for export AWS credentials
  ![Copy credentials to the clipboard](https://github.com/kevincloud/credhelper/blob/master/docs/images/clipboard.png)
* Go back to your command line and run `python credhelper.py`

You should see all the workspaces where credentials are being changed.

If you have any feedback or trouble using the app, please open an issue and I'll work diligently to get it resolved.

Enjoy!
