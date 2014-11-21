isup-notify
===========
##Install sendgrid and cron

```
sudo apt-get install python-pip cron
sudo pip install sendgrid

```

Note: You should have created a sendgrid account. You can do it  here: https://sendgrid.com/user/signup

##Setting up your new crontab

Inside your home directory run:

```
crontab -e

```
then add the new crontab at the end of the file.

It must look like this:

```
0 */6 * * * python /home/user/isup-notify/main.py
```
or:
```
0 */6 * * * python /home/iliana/isup-notify/main.py > /home/user/isup.log 
```
The first one runs the file main.py every 6 hours.
The second one runs the file main.py every 6 hours but also writes every result of the print command into the file isup.log

You can find more about cron in the Unix man pages (man cron , man crontab) and here : http://www.linuxhelp.net/guides/cron/
