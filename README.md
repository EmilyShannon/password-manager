# Password Manager

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)

    0. [Configuring the database](#config)
    1. [Adding a New Password](#add)
    2. [Retrieving a Password](#retrieve)
    3. [Deleting a Password](#delete)
    4. [Generating a Password](#gen)

## Introduction <a name="introduction"></a>

This is a password manager CLI application that helps you securely store and manage your passwords. 

### How it works 

1. Input your master password. It is important to remember this and keep it somewhere secure. 
2. The program hashes your password (i.e. converts it to a unique string 64 characters long). It also creates a device secret, which is a random string of 10 characters. The masterkey is derived from the hashed password and device secret using the [PBKDF2 algorithm](https://cryptobook.nakov.com/mac-and-key-derivation/pbkdf2). Generating the key this way protects your hashed master password from [dictionary attacks](https://en.wikipedia.org/wiki/Dictionary_attack) and [rainbow table attacks](https://en.wikipedia.org/wiki/Rainbow_table). 
3. Once your master password is configured successfully, you can add, retrieve or delete passwords. Your passwords are encrypted and decrypted using the [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) algorithm and the master key.   

This application uses a <b>MariaDB</b> database to store a user's passwords. See [here](https://www.mariadbtutorial.com/getting-started/install-mariadb/) for instructions to install and configure MariaDB.  

## Features <a name="features"></a>

- Securely store passwords
- Generate strong passwords
- Search and retrieve passwords quickly

## Installation <a name="installation"></a>

To install the password manager, follow these steps:

1. Clone the repository: `git clone https://github.com/EmilyShannon/password-manager.git`
2. Create a Conda env and install the required dependencies: `conda create --name <env_name> --file requirements.txt`

## Usage <a name="usage"></a>

First, ensure that the Conda environment you created is active. 

### Configuration <a name="config"></a>

Run `config.py`, either from your IDE or running `python src/config.py` in the terminal (assuming you are in the password-manager directory). This application requires you to create a <i>master password</i>. You will be prompted to do so. Store your master password as you will need to use this to access your other passwords later on. After this step is complete, your database is configured! 

### Creating, adding, retreiving and deleting passwords

To run the application, you need to run `password_manager.py` with command line arguments as follows: 

1. <b>To add a new password: </b> <a name="add"></a>

Run `password_manager.py a --site <site_name> --login <username> --url <site_url>` 
 - `site_name` should be the name of the site or service this password is for, e.g. 'github'.
 - `username` should be your username on this site, e.g. 'EmilyShannon'.
 - `url` should be the link to the site, e.g. 'https://github.com/'.

2. <b>To retrieve an existing password: </b> <a name="retrieve"></a>

Run `password_manager.py r --site <site_name> --login <username> --url <site_url> --email <email_address>` 
 - `site_name` should be the name of the site or service this password is for, e.g. 'github'.
 - `username` should be your username on this site, e.g. 'EmilyShannon'.
 - `url` should be the link to the site, e.g. 'https://github.com/'. 
 - `email_address` is the email address associated with the account.

 Note that it is not required to enter all of these fields, the results will be any entries matching the arguments provided. 

3. <b>To delete an existing password: </b> <a name="delete"></a>

Run `password_manager.py d --site <site_name> --login <username> --url <site_url> --email <email_address>` 
 - `site_name` should be the name of the site or service this password is for, e.g. 'github'.
 - `username` should be your username on this site, e.g. 'EmilyShannon'.
 - `url` should be the link to the site, e.g. 'https://github.com/'.
 - `email_address` is the email address associated with the account.

 Note that it is not required to enter all of these fields, any entries matching the arguments provided will be deleted. 

4. <b>To generate a new password: </b> <a name="gen"></a>

Run `password_manager.py g --length <pass_length>` 
 - `pass_length` how long you need your password to be. The default is 16.