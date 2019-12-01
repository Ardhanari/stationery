## Testing of Papeire

### Manual testing

I was lucky enough to have testers who were more than eager to test this project during the development and after it was deployed on Heroku. Below is the record of all things that were tested to make sure all parts of the website are fully functional.

#### General UI elements
Testers had:
- Clicked shop's name to return to the homepage
- Clicked each link in the navbar to check if it leads to correct page
- Tested that different navbar elements are visible to logged in ('Profile', 'Log out') and anonymous users ('Sign up', 'Log in') while 'Products', 'Search' and 'Your cart' are visible for all users. 
- Clicked all links in the footer to make sure they open in a new window and point to the correct page

##### Cart:
- add an item to the cart being logged in, 
- and logged out,
- add more than one product by clicking 'add to cart' few times, 
- edit the number of products in the cart, 
- when the number of product in the cart is bigger than its quantity in stock, user is given feedback on this and cannot order more products than available even if not taking any action
- remove the item from the cart by setting its quantity to 0
- check if the numbers for a total price are correct for the selected number of products
- the number of products in cart displayed in navbar changes accordingly 

###### Checkout:
- on all stages of checkout summary of the cart is visible and provides correct information
- button leading to checkout stage is active and points to the correct page
- shipping address form is easy to understand and fill
- user can't submit an invalid form
- shipping address will be saved by clicking 'proceed to checkout'
- form for credit card payment accepts correct payment information and declines incorrect providing feedback 

##### Breadcrumbs
- made sure that all breadcrumbs are accurate and clicked the links to test them pointing to correct pages

##### Products pages
- Used categories selection to navigate between categories and all product pages
- Used search to search for products and return relevant results
- Used sorting dropdown to sort the products by price and date added
- Clicked on item picture and item title to confirm both lead to the detailed product page
- Deailed product page display product picture, description, price, rating and reviews correctly. 
- Only logged in users can rate the product using stars rating. 

##### Static pages 
- picture and text display correctly on 'About me' and 'FAQ'
- tested that link on 'About me' leads to 'FAQ'
- link on 'FAQ' leads to 'About me'
- contact form sends an email containing all information provided by user to the dedicated Gmail account 
- contact form can be used by anonymous users as well

##### Authentication and user profile
- User can register to the website
- User can log in using the same credentials provided during registration
- user can view their profile, even if they took no action in the shop yet
- user can view a list of their orders if there are any
- their orders link to order summary page where information on the product bought
- on order summary page user can write a review of the product they bought
- they can also edit the review after adding
- if user wrote a review, it is displayed in the order summary as well
- user can see their shipping address
- user can edit their shipping address if necessary
- form for editing address won't be submitted if invalid
- user can request password reset 
- logging out provides feedback to the user they were logged out


#### Bugs found during testing

The price of the product would stay the same no matter the quantity of it in the cart. Solved by adding relevant code. 

Google Dictionary (chrome extension) would break the website, returning occasionally 404 and 403 errors when browsing pages, and '403 CSRF token missing' when submitting any form (including 'add to cart'). Solved by first testing the same steps on a different browser, when confirmed it's Chrome problem turning off the extensions and tracking down the one responsible for all of this. 
Solved by reinstalling the extension to clean version. 

Rendering page with no reviews would return error 500 on Heroku. Saving the address details during checkout would return the same. 
These two issues are together because despite how different they are, their source was the same. I provisionally fixed the first issue by changing the database query, when previous code would be returned with "column does not exist". The column in question was in the schema and model for the reviews table, however, I bravely assumed, since there is no reviews in the database yet, simple rewording of the query would be enough. 
However, the same problem (ProgramaticError, Column does not exist) arose for the shipping address. This time I couldn't assume the same since in the database there were already shipping addresses from the previous testing. I knew there is column 'user_id' because I was staring at it, reading directly from the database. 
So I kept digging and after 3.5 hours down the rabbit hole, I found myself reading about recovering data from corrupted databases. At this point, I realised it will be easier and faster to drop the old DB (since tests were conducted on fake products and fake accounts) and try to replicate the same bug on the clean database made from scratch. And lo and behold, there were no ProgramaticErrors (or any errors for that matter) showing up when saving and reading from the database. 
After that discovery, I felt dragged but also really relieved it was _just that_ (I must admit, part of the relief was coming from the fact, that I was in this comfortable position where I could just drop DB and not look back)

##### UX/UI 

- No clue as to where add user reviews and how to do that. This will be addressed soon, after finding the best place to do it.
- Inconsistency between fonts in the headings. Solved by unifying all headings to use Fanwood Text

### Travis CI
For the love of all good things in this world, I couldn't make Travis notice this repository as something suitable for testing. Following the documentation, granting permissions from GitHub, uploading `.travis.yml` in different versions, giving it time (in case it needs it) and the dashboard is still empty and no build is built. 
After troubleshooting it for a little while, I decided to continue with the project submission and find a solution to this issue in the foreseeable future. Track of old versions of `.travis.yml` can be found in this repository's commits, however the file is removed for now. 