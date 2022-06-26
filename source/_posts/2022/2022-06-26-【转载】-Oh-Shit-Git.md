---
title: 【转载】Oh Shit, Git!?!
categories: 技术
tags: 
  - Git
date: 2022-06-26
toc: true
---

原文链接： [https://ohshitgit.com/](https://ohshitgit.com/)

Git is hard: screwing up is easy, and figuring out how to fix your mistakes is fucking impossible. Git documentation has this chicken and egg problem where you can't search for how to get yourself out of a mess, *unless you already know the name of the thing you need to know about* in order to fix your problem.

So here are some bad situations I've gotten myself into, and how I eventually got myself out of them *in plain english.*

### Oh shit, I did something terribly wrong, please tell me git has a magic time machine!?!

```bash
git reflog
# you will see a list of every thing you've
# done in git, across all branches!
# each one has an index HEAD@{index}
# find the one before you broke everything
git reset HEAD@{index}
# magic time machine
```

You can use this to get back stuff you accidentally deleted, or just to remove some stuff you tried that broke the repo, or to recover after a bad merge, or just to go back to a time when things actually worked. I use `reflog` A LOT. Mega hat tip to the many many many many many people who suggested adding it!

### Oh shit, I committed and immediately realized I need to make one small change!

```bash
# make your change
git add . # or add individual files
git commit --amend --no-edit
# now your last commit contains that change!
# WARNING: never amend public commits
```

This usually happens to me if I commit, then run tests/linters... and FML, I didn't put a space after an equals sign. You could also make the change as a new commit and then do rebase -i in order to squash them both together, but this is about a million times faster.

*Warning: You should never amend commits that have been pushed up to a public/shared branch! Only amend commits that only exist in your local copy or you're gonna have a bad time.*

### Oh shit, I need to change the message on my last commit!

```
git commit --amend
# follow prompts to change the commit message
```

Stupid commit message formatting requirements.

### Oh shit, I accidentally committed something to master that should have been on a brand new branch!

```
# create a new branch from the current state of master
git branch some-new-branch-name
# remove the last commit from the master branch
git reset HEAD~ --hard
git checkout some-new-branch-name
# your commit lives in this branch now :)
```

Note: this doesn't work if you've already pushed the commit to a public/shared branch, and if you tried other things first, you might need to `git reset HEAD@{number-of-commits-back}` instead of `HEAD~`. Infinite sadness. Also, many many many people suggested an awesome way to make this shorter that I didn't know myself. Thank you all!

### Oh shit, I accidentally committed to the wrong branch!

```
# undo the last commit, but leave the changes available
git reset HEAD~ --soft
git stash
# move to the correct branch
git checkout name-of-the-correct-branch
git stash pop
git add . # or add individual files
git commit -m "your message here";
# now your changes are on the correct branch
```

A lot of people have suggested using `cherry-pick` for this situation too, so take your pick on whatever one makes the most sense to you!

```
git checkout name-of-the-correct-branch
# grab the last commit to master
git cherry-pick master
# delete it from master
git checkout master
git reset HEAD~ --hard
```

### Oh shit, I tried to run a diff but nothing happened?!

If you know that you made changes to files, but `diff` is empty, you probably `add`-ed your files to staging and you need to use a special flag.

```
git diff --staged
```

File under ¯\_(ツ)_/¯ (yes, I know this is a feature, not a bug, but it's fucking baffling and non-obvious the first time it happens to you!)

### Oh shit, I need to undo a commit from like 5 commits ago!

```
# find the commit you need to undo
git log
# use the arrow keys to scroll up and down in history
# once you've found your commit, save the hash
git revert [saved hash]
# git will create a new commit that undoes that commit
# follow prompts to edit the commit message
# or just save and commit
```

Turns out you don't have to track down and copy-paste the old file contents into the existing file in order to undo changes! If you committed a bug, you can undo the commit all in one go with `revert`.

You can also revert a single file instead of a full commit! But of course, in true git fashion, it's a completely different set of fucking commands...

### Oh shit, I need to undo my changes to a file!

```
# find a hash for a commit before the file was changed
git log
# use the arrow keys to scroll up and down in history
# once you've found your commit, save the hash
git checkout [saved hash] -- path/to/file
# the old version of the file will be in your index
git commit -m "Wow, you don't have to copy-paste to undo"
```

When I finally figured this out it was HUGE. HUGE. H-U-G-E. But seriously though, on what fucking planet does checkout -- make sense as the best way to undo a file? :shakes-fist-at-linus-torvalds:

### Fuck this noise, I give up.

```
cd ..
sudo rm -r fucking-git-repo-dir
git clone https://some.github.url/fucking-git-repo-dir.git
cd fucking-git-repo-dir
```

Thanks to Eric V. for this one. All complaints about the use of `sudo` in this joke can be directed to him.

For real though, if your branch is sooo borked that you need to reset the state of your repo to be the same as the remote repo in a "git-approved" way, try this, but beware these are destructive and unrecoverable actions!

```
# get the lastest state of origin
git fetch origin
git checkout master
git reset --hard origin/master
# delete untracked files and directories
git clean -d --force
# repeat checkout/reset/clean for each borked branch
```

*Disclaimer: This site is not intended to be an exhaustive reference. And yes, there are other ways to do these same things with more theoretical purity or whatever, but I've come to these steps through trial and error and lots of swearing and table flipping, and I had this crazy idea to share them with a healthy dose of levity and profanity. Take it or leave it as you will!

---

Many thanks to everyone who has volunteered to translate the site into new languages, you rock! [Michael Botha](https://github.com/michaeljabotha) ([af](https://ohshitgit.com/af)) · [Khaja Md Sher E Alam](https://github.com/sheralam) ([bn](https://ohshitgit.com/bn)) · [Eduard Tomek](https://github.com/edee111) ([cs](https://ohshitgit.com/cs)) · [Moritz Stückler](https://github.com/pReya) ([de](https://ohshitgit.com/de)) · [Franco Fantini](https://github.com/francofantini) ([es](https://ohshitgit.com/es)) · [Hamid Moheb](https://github.com/hamidmoheb1) ([fa](https://ohshitgit.com/fa)) · [Senja Jarva](https://github.com/sjarva) ([fi](https://ohshitgit.com/fi)) · [Michel](https://github.com/michelc) ([fr](https://ohshitgit.com/fr)) · [Alex Tzimas](https://github.com/Tzal3x) ([gr](https://ohshitgit.com/gr)) · [Elad Leev](https://github.com/eladleev) ([he](https://ohshitgit.com/he)) · [Aryan Sarkar](https://github.com/aryansarkar13) ([hi](https://ohshitgit.com/hi)) · [Ricky Gultom](https://github.com/quellcrist-falconer) ([id](https://ohshitgit.com/id)) · [fedemcmac](https://github.com/fedemcmac) ([it](https://ohshitgit.com/it)) · [Meiko Hori](https://github.com/meih) ([ja](https://ohshitgit.com/ja)) · [Zhunisali Shanabek](https://github.com/zshanabek) ([kk](https://ohshitgit.com/kk)) · [Gyeongjae Choi](https://github.com/ryanking13) ([ko](https://ohshitgit.com/ko)) · [Rahul Dahal](https://github.com/rahuldahal) ([ne](https://ohshitgit.com/ne)) · [Martijn ten Heuvel](https://github.com/MartijntenHeuvel) ([nl](https://ohshitgit.com/nl)) · [Łukasz Wójcik](https://github.com/lwojcik) ([pl](https://ohshitgit.com/pl)) · [Davi Alexandre](https://github.com/davialexandre) ([pt_BR](https://ohshitgit.com/pt_BR)) · [Catalina Focsa](https://github.com/catalinafox) ([ro](https://ohshitgit.com/ro)) · [Daniil Golubev](https://github.com/dadyarri) ([ru](https://ohshitgit.com/ru)) · [Nemanja Vasić](https://github.com/GoodbyePlanet) ([sr](https://ohshitgit.com/sr)) · [Björn Söderqvist](https://github.com/cybear) ([sv](https://ohshitgit.com/sv)) · [Kitt Tientanopajai](https://github.com/kitt-tientanopajai) ([th](https://ohshitgit.com/th)) · [Taha Paksu](https://github.com/tpaksu) ([tr](https://ohshitgit.com/tr)) · [Andriy Sultanov](https://github.com/LastGenius-edu) ([ua](https://ohshitgit.com/ua)) · [Tao Jiayuan](https://github.com/taojy123) ([zh](https://ohshitgit.com/zh)) . With additional help from [Allie Jones](https://github.com/alliejones) · [Artem Vorotnikov](https://github.com/vorot93) · [David Fyffe](https://github.com/davidfyffe) · [Frank Taillandier](https://github.com/DirtyF) · [Iain Murray](https://github.com/imurray) · [Lucas Larson](https://github.com/LucasLarson) · [Myrzabek Azil](https://github.com/mvrzvbvk)

If you'd like to help add a translation into your language, submit a PR on [GitHub](https://github.com/ksylor/ohshitgit)