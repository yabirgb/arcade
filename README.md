# arcade

Yet another static site generator. 

## Porpouse

The porpouse in life for this project is to create a cool
static site for my blog

## How to use

1. Create a new project

```
arcade init
```

2. Modify the configuration file. An example is 

```
author_name: 'Yábir García Benchakhtir'
base_path: 'http://localhost:5500'
page_name: "Yabir Garcia's Blog"
theme: 'themes/baseline'
social:
  email:
    icon: 'fa-envelope'
    url: 'mailto:yabirg@protonmail.com'
  github:
    icon: 'fa-github'
    url: 'https://github.com/yabirgb'
  linkedin:
    icon: 'fa-linkedin-square'
    url: 'https://www.linkedin.com/in/yabirgb/'
  mastodon:
    icon: 'fa-mastodon'
    url: 'https://mstdn.io/@yabirgb'
  twitter:
    icon: 'fa-twitter'
    url: 'https://twitter.com/yabirgb'
```

3. Create a index file

Go to the `content` and create an file called `index.md`. This will
be the entry point to your blog

4. Build or watch your project

```
arcade build
arcade watch
```
