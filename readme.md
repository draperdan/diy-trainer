# DIY-Trainer Readme

## Description

This repository contains the Django project (v1.6) and applications powering the diy-trainer.com website. This website is a fictitious DIY knowledge-base startup to test consumer preferences.

The website is split across two subdomains. One domain drives the "guides" test while the other drives "projects." This configuration is evident in the settings, which have not been pushed to this repo. This will be more clear when looking at the `urls.py` files for the project and apps.

I've published this code to Github for the benefit of the Django community. It will not be actively developed, though I'm happy to answer any questions about the code.

## Usage

1.  Install the requirements as listed in the `requirements.txt` file. I highly recommend doing this in a virtualenv.
2.  Create your settings using either the default Django settings or from a source such as [two-scoops](https://github.com/twoscoops/django-twoscoops-project).
3.  Create a database by running `./manage.py syncdb` in addition to your migrations from South.
4.  Fire up a dev server with `./manage.py runserver`

## Author notes

All code was written by [Patrick Beeson](http://patrickbeeson.com). No images or design included in this repository may be used without permission.