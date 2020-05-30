The application requires a few different components to build. The program uses flask to run application.py, which uses functions from
helpers.py. This creates the basic structure, in which are inserted the html templates.

HTML Templates
The basic template of each page is layout.html which contains information that is common to all pages, for example the navbar and the
containers in which other content goes. index.html is the template for the home page, which is also the page which will display the
constructed meal plans. login.html corresponds to the login page, while register.html contains the form required to register an account
on the website. Finally, options.html contains the form for changing your preferences, corresponding to the Update Preferences page, and
progress.html displays your current preferences. Each of the html templates which contain a form also have Javascript functions which provide
alerts if one piece of information was not entered by the user, since all pieces of information are necessary to calculate the meal plans.
Bootstrap and a css style sheet called styles.css where used to make the website look nicer. The Jumbotron in particular was used, as was
Google Fonts to find a more interesting font to use for the webstite's aesthetic.

fit.db
This database contains one table, users, which contains important user information. The fields are as follows: id for unique identification
of each user, username for their usernames, hash for the hashed values of passwords. Weight, height, sex, dietary, plan, age, activity, hall
are all inputs that are taken at registration and can be changed by using the Update Preferences page. These inputs are what are used to
calculate BMR and estimated calories/day, the latter of which is stored in the bmr field. All these fields are important in the selection of
foods for the generated meal plans.

HUDS API
I needed access to the HUDS API to provide me with data of which foods were offered at each hall that day, as well as the recipes for each
of these foods, which provides important macronutrient information. I queried the API using Postman, using credentials which were helpfully
approved for me by their software management team. I was then able to make requests to the API and the data returned was parsed for my application

Application.py
The main body of the code and the application lies in this file. I will describe each function that follows the initial modules and some basic
setup functions that were used in the finance pset. By default, when you open the app, it should direct you to the register page. The next two
functions work in tandem to produce the meal plans and the home page. Looking at index() first, it first extracts three pieces of data from the
database based on who is currently logged in. These three pieces of data, the estimated total number of calories per day, the dietary preference,
and where the person will eat, summarize the information needed to generate each personalised meal plan. The first thing that happens is each hall
is associated with their unique location id, which is needed to format the query to the HUDS api, which I was very kindly given access to. Next comes
the API query, which was formatted for me by Postman. The only addition is the changeable value of the location id, depending on where the person was
eating. Included in the Headers is my unique key for authorisation to access the API, which used Oauth authorisation. The query was to "recipes", which
would return all recipes for all the food at that hall for the next few days. This had to be translated from JSON into a usable format, and I stored it
within a list text1. Next, I parsed the data to only use the recipes for the current day and to split the groups of foods into if they were offered for
breakfast, lunch or dinner. I also separated vegetarian food from all foods at this point. Next, I had a separate function checking(), which would
generate the meal plan. At this stage, the plan generation algorithm is very simple. It takes a random number between 4 and 7 (6 and 10 if you're
vegetarian because you need to eat more to get the required number of calories and nutrients) and randomly picks that many foods from the list of recipes.
With this random list of foods, a check is run to ensure it is a decently healthy choice. To judge this, the total calories, fat, protein, and carbohydrate
content needed to be within certain bounds. A standard recommended balanced diet consists of 25-35% protein, 20-35% fat, 35-45% carbohydrates, so this was
the target around which flexible bounds were inserted. Since each person eats snacks as well as meals, I estimated that a quarter of the total number
of calories for one day should be consumed at each meal, which leaves around another quarter of the total number of calories for snacks. If the
list of foods passed this test, then it would be returned to the index() function, if not, then the whole function begins again and generates a new set
of random numbers. Once data for each meal is eventually passed back to the index() function, a final check on each of the macronutrient contents is
made, which will inform the user of what sort of foods to be looking at and avoiding in their snacks. Finally, the homepage can be constructed, which
displays the three food plans, as well as calorie information and macronutrient advice. Each time you refresh the page, a new meal plan is produced,
which makes sense for now since you can get some pretty interesting sounding meal plans.

Login, check, options, and progress are fairly straightforward functions which either display pretty static information or do simple tasks. The main
important part of register, apart from taking in data, is how it calculates your BMR (Basal metabolic rate) and estimates calories/day from this.
The formula in the code is the Harris-Benedict formula for BMR. From this basal metabolic calorie consumption, 500 calories are added if the
user wishes to gain weight, and 500 calories are deducted if they wish to lose weight. This is because 500 calories corresponds to losing or gaining
a pound of weight a week, which is a healthy and steady way to lose or gain weight.

Improvements
The main improvements are to do with the meal generating algorithm. Right now, there is a random system of choosing foods, which allows
for odd combinations and foods that people might not like. To tackle this issue, I would first make sure there was an entree in each meal,
which currently is already the case in the majority of the meals, but not necessarily. A rating system could be implemented for each food,
so that if you gave one food a really low rating, it wouldn't appear anymore, and a really high rated food, or foods related to that highly
rated food, could appear more often in your plan. This could use a mchine-learning algorithm, and ratings could be cumulated across users to
give an overall rating that new users could look at to decide whether they want to try that meal plan. Grouping the foods would also be
important, so that your meal plan doesn't offer you pancake syrup without pancakes.
