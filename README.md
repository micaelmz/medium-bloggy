
![Medium Bloggy](assets/images/game-logo.PNG)

![Medium Bloggy Responsive](assets/testing/results/amiresponsive.PNG)

- [Overview](#overview)
- [UX](#ux)
  - [User Stories](#user-stories)
  - [Design](#design)
    - [Color Scheme](#color-scheme)
    - [Icons](#icons)
    - [Typography](#typography)
  - [Wireframes](#wireframes)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Features](#future-features)
- [Technologies Used](#technologies-used)
  - [Front-End Technologies](#front-end-technologies)
  - [Miscellaneous Technologies](#miscellaneous-technologies)
- [Agile Project Management](#agile-project-management)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
  - [Media](#media)
  - [Acknowledgments](#acknowledgments)

<br/>

---

## Overview

Medium Bloggy is a place for bloggers/writers to show-case their work. You can view the deployed site [here]().

<br/>

## UX

This project is part of the [Code Institute](https://codeinstitute.net/) Full Stack Software Development course, specifically **Module 3: Data Centric Development**. 

The objective for this milestone project is to "*build a full-stack site that allows your users to manage a common dataset about a particular domain*".

<br/>

### User Stories

- User Stories were written from the perspective of the user:
    - the registered user that wants to write articles or comment on other articles. 
    - the non-registered user that just wants to read blog articles, without contributing content. 
    - the site administrator.

<br/>

"**__As a *registered user*, I__** ______________________________________________"

- should be able to register an account with the site in order to publish articles. 
- should be able to create a blogger portfolio page, with relevant details. 
- should be able to CRUD my portfolio page. 
- should be able to CRUD articles from my portfolio. 
- should be able to see how many views my articles have received. 
- should be able to see how many likes my articles have received.
- should be able to reply to any comments written about my articles.
- should be able to make comments on other blog articles. 

"**__As a *non-registered user*, I__** ______________________________________________"

- should be presented with blog article on the main page. 
- should be able to click on an article on the main page to read more about it. 
- should be able to search through articles. 
- should be able to click on the author of the blog to find out more details about them.

"**__As an *administrator*, I__** ______________________________________________"

- should have an adminstrator account setup. 
- should be able to see an administrator dashboard page. 
- should be able to see a list of all blog items, with relevant details. 
- should be able to see a list of all blog authors, with relevant details.

<br/>

### Design


<br/>

#### Color Scheme

- ![#800080](https://placehold.it/15/800080/800080) purple text/background
- ![#B22234](https://placehold.it/15/B22234/B22234) red button
- ![#FFFF00](https://placehold.it/15/FFFF00/FFFF00) yellow button/text
- ![#00C0A3](https://placehold.it/15/00C0A3/00C0A3) green text
- ![#02AFFF](https://placehold.it/15/02AFFF/02AFFF) blue dashboard (score, level, lives)
- All of these colors are set at `:root` level within the [style.css](assets/css/style.css) file. The use of css custom properties (variables) is in keeping with the principles of DRY.


#### Icons

- [Font Awesome 5.6.1](https://fontawesome.com/) icons are used in the [how to play](how-to-play.html) page, and in the gamepad controller buttons.

<br/>

#### Typography

- [Google Fonts](https://fonts.google.com/) were used across the site, namely:
  - [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) : game title and menu buttons.

<br/>

### Wireframes

- Wireframes were created using [Balsamiq Wireframes](https://balsamiq.com/) and can be viewed by clicking on links below.

<br/>


|    Home Page   |    Sound-Options.html     |    High-Scores.html    |
|    :----:      |    :----:                 |    :----:              |
|[Desktop/Mobile](wireframes/home-page.png)|[Desktop/Mobile](wireframes/sound-options.png)|[Desktop/Mobile](wireframes/high-scores-page.png)|

<br/>

---

## Features

### Existing Features
  - **Administrator Dashboard:** displaying Art, Artists. 


<br/>

### Future Features
A full list of future features **can be viewed in the [Product Backlog](https://github.com/leithdm/milestone-project-3/projects/1)**, but we will briefly mention some of them here:
-  **Menu Items:** high score Leaderboard, e.g. top 10 high scores.


<br/>

---

## Technologies Used

### Front-End Technologies

- [HTML5](https://en.wikipedia.org/wiki/HTML5) - used to provide content and structure.
- [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - used to provide styling.
- [JavaScript ES6](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - the game is built entirely from vanilla JavaScript.
- [Google Fonts](https://fonts.google.com/) - used to provide font styling.
- [Am I Responsive?](http://ami.responsivedesign.is/) - used to show site responsiveness.

<br/>

### Miscellaneous Technologies

- [VS Code](https://code.visualstudio.com/) - used as the primary IDE.
- [GitHub](https://github.com/) - used for remote storage of code.
- [TinyPNG](https://tinypng.com/) - used to optimize (.jpg, .png) images for faster loading.
- [Balsamiq](https://balsamiq.com/) - used to create the project's wireframes.

<br/>

---

## Agile Project Management

[GitHub Projects](https://github.com/features/project-management/) was used to iteratively sprint through the development of this app. Each *User Story* became an individual *Issue*, and was placed in a Kanban board composed of the following columns:
1. **Backlog** - all user stories, ordered by value/priority.
2. **Sprint** - a subset of user stories to be completed in a x1 week sprint.
3. **In Progress** - user stories currently being worked on from current sprint.
4. **Done** - user stories completed, and tested.

Along with tracking user stories, Github Projects was also used to track bugs. **The full list of user stories/bugs can be viewed [here](https://github.com/leithdm/milestone-project-3/projects/1).**

![GitHub Projects in action](wireframes/agile-project-management.png)

<br/>

---

## Testing

The testing process can be viewed [here](TESTING.md).

<br/>

---

## Deployment

**How to deploy**

To deploy this page to GitHub Pages from its [GitHub repository](https://github.com/leithdm/milestone-project-3), the following steps were taken:

1. From the menu items near the top of the page, select **Settings**.
2. Scroll down to the GitHub **Pages** section.
3. Under **Source** click the drop-down menu labelled **None** and select **Master Branch**.
4. The page refreshes automatically, and the website is now deployed.
5. Scroll back down to the **GitHub Pages** section in **Settings** to retrieve the link to the deployed website. It may take a short time to go live, but typically < 60 seconds.

<br/>

**How to run locally:**

To clone this project from GitHub:

1. Under the repository’s name, click **Clone or download**.
2. In the **Clone with HTTPS** section, copy the given URL.
3. In your IDE of choice, open **Git Bash**.
4. Change the current working directory to the location where you want the cloned directory to be made.
5. Type **git clone**, and then paste the URL copied in Step 2

`git clone https://github.com/leithdm/milestone-project-3.git`

1. Press **Enter**. Your local clone will be created.

<br/>

---

## Credits

### Media

- Images:
  - The [background image]([https://link](http://www.classicgaming.cc/classics/asteroids/graphics)) used in the game menu was again provided by [Classic Gaming](http://www.classicgaming.cc/classics/asteroids/). A filter was applied to darken the image.
  - The in-game star background was provided by [Jake Weirick](https://unsplash.com/photos/Q_RBVFFXR_g) via [Unsplash](https://unsplash.com/).
  - The patterned background visible on desktop was provided by [Hero Patterns](http://www.heropatterns.com/).
- Game Programming Tutorials:
  - [Make JavaScript Asteroids in One Video](https://www.youtube.com/watch?v=HWuU5ly0taA&ab_channel=DerekBanas): a great introductory video.
  - [Code Asteroids in JavaScript (1979 Atari game) - tutorial](https://www.youtube.com/watch?v=H9CSWMxJx84&ab_channel=freeCodeCamp.org): another excellent tutorial.
  - [Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial) tutorials provided by [MDN web docs](https://developer.mozilla.org/en-US/).
  - [Code Your First Game: Arcade Classic in JavaScript on Canvas](https://www.udemy.com/course/code-your-first-game/): a free course on [Udemy](https://www.udemy.com/).
  - [How to Program Games: Tile Classic in JS for HTML5 Canvas](https://www.udemy.com/course/how-to-program-games/): a paid course on [Udemy](https://www.udemy.com/).


<br/>

### Acknowledgments

- [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/?originalSubdomain=ng) - for his mentorship and guidance.