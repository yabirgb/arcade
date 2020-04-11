# arcade

![](assets/hartmut-tobies-O9TEKuI1Icw-unsplash-min.jpg)

Yet another static site generator. 

## Features

- Theme customization (templates use `jinja2`)
- Live reload while editing
- Customizable paths

## Installation

```
pip install arcade-generator
```

## Commands

- Create a new site
```
arcade init
```

- Compile your site
```
arcade build
```   
- Watch local project
```
arcade watch
```


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

## Themes

Currently only the baseline theme is available. You can download it [here](https://github.com/yabirgb/arcade/releases/download/0.0.5/baseline.zip)

Made with :heart: and :snake: by Yábir Benchakhtir

## Credit

Photo by [@hartmuttobies](https://unsplash.com/@hartmuttobies)
