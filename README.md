# gret_notes

Project for personalized notes.

## Test-site on the pythoneverywhere server:

TBD

## Idea:

 App for notes with option to make it fast and ergonomic.
 Options to build up old notes, with fast recognizing, what note you want to expand.
 Sharing content, to make possibility of working in groups.
 Connecting both options - to make possible providing system of fast information exchange, within teams.

## Features:

* **Notes**
    * [X] Basic notes - index page with listing
        * [X] new/edit/delete functions
    * [X] Tagging - primal note's organization - [django-taggit package](https://django-taggit.readthedocs.io/en/latest/index.html)
        * [ ] Search notes by tags
        * [ ] Links for fast adding and deleting note's tags
    * [ ] Grouping - more organization for your notes (to allow sharing the whole group)
    * [ ] Pinup - fast links to most important/urgent cases
        * [ ] List by set up expiration time or priority
    * [ ] Dividing notes into sections with different permissions per user for each section
    * [ ] Priority / flags / statuses for notes

* **User / Teams:**
    * [X] Basic user authorization - [Django authentication system](https://docs.djangoproject.com/en/3.0/topics/auth/default/)
        * [ ] Groups management interface
    * [X] Object permissions for users - [django-guardian package](https://django-guardian.readthedocs.io)
        * [ ] Transferring notes / groups to another user
        * [ ] Object permissions for groups
    * [ ] Profile page

* **Other:**
    * [ ] Filters for displayed objects
    * [ ] Error screens
    * [ ] Implementing rich text editor
    * [ ] Checklists / Next step lists (stand alone from notes)
        * [ ] Checklists / Next step lists - build into notes
    * [ ] Data serialization - moving bunch of notes system 

## Main sources of knowledge:

* https://docs.djangoproject.com
* https://hackersandslackers.com
* https://django-guardian.readthedocs.io
