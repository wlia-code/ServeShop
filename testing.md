## Manual Testing

This section of the documentation consists of various manual tests and online validators to assess the quality of the code and to ensure the functionality of the GN-SHOP project.

---

### Stripe

To test the checkout payments with card details in test mode, I used the following long card numbers:

- **4242424242424242**: for successful card payments (Visa)

The above test was performed successfully, and Stripe integration is confirmed to be working as expected.

<br></br>

### Home/Index
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| Logo/Home Link      | Click on Logo at the top of the page | Redirect to the home page                                | PASS   |
| All Products Link   | Click on the middle nav link    | Opens the Products Page                                 | PASS   |
| Fashion Link        | Click on the middle nav link    | Opens the category Fashion Page                         | PASS   |
| Accessories Link    | Click on the middle nav link    | Opens the category Accessories Page                     | PASS   |
| Sale Link           | Click on the middle nav link    | Opens the Sale Page                                     | PASS   |
| Collections Click   | Click on the middle nav link    | Opens a dropdown with each collection's links           | PASS   |
| My Account Icon     | Click on the nav link           | Opens a dropdown with other links                       | PASS   |
| Shopping Bag Icon   | Click on the nav link           | Opens the Bag Page                                      | PASS   |
| Shop Now Button     | Click on the main section button | Opens the Products Page                                 | PASS   |

### Featured Collection Section
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| See More Button     | Click on the Featured Collection Section button | Redirect to the specific collection page         | PASS   |

### Contact Section
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| Send Message Button | Click on the Contact Section button | Redirect to the Contact page                        | PASS   |

### Footer
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| Media links         | Click on link                  | Open a blank page to the clicked link                   | PASS   |

### Contact
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| Submit Form         | Attempt to submit a blank form  | Form validation prevents submission and alerts the user | PASS   |
| Submit Form         | Attempt to submit with one input filled in | Form validation prevents submission and alerts the user | PASS   |
| Email input         | Enter an invalid email address  | Form will not send and user is prompted for a valid email | PASS   |
| Submit Valid Form   | Submit a complete and valid form | Page reloads and displays a success message              | PASS   |
| Admin Panel         | Check submission in the Admin Panel | Information stored correctly in the database           | PASS   |

### Profile
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| Profile Link        | Check when logged out          | Profile page is not accessible to users not logged in   | PASS   |
| Profile Link        | Click when logged in           | Redirects user to their profile page                    | PASS   |
| Update Button       | Click Update Button            | The profile is updated and saved                        | PASS   |
| Input fields        | Enter invalid inputs           | User receives an error message                          | PASS   |
| Input fields        | Enter valid inputs             | User is informed that the profile saved successfully    | PASS   |

### Authentication
| Test                | Method                         | Expected Outcome                                       | Result |
|---------------------|--------------------------------|--------------------------------------------------------|--------|
| Sign Up             | Create an account              | Prompted to wait for admin email confirmation           | PASS   |
| Login               | Login with a registered account | Redirected to homepage with a login success message     | PASS   |
| Remember Me         | Click Remember Me before logging in | User stays logged in on the next visit                | PASS   |
| Forgot Password     | Submit email via Forgot Password | Password reset link sent to the user's email            | PASS   |

### Basket and Bag
| Test                    | Method                         | Expected Outcome                                       | Result |
|-------------------------|--------------------------------|--------------------------------------------------------|--------|
| Basket Icon             | Click on Basket icon in the nav | Redirects to the bag page                               | PASS   |
| Basket Page with no items| Open basket page without items | Displays a message indicating an empty basket           | PASS   |
| Item in Basket          | Add an item to the basket       | Item appears in the basket                              | PASS   |
| Multiple items in Basket| Add multiple items              | All items and quantities are updated correctly          | PASS   |
| Delete Item in Basket   | Click 'Delete' button           | Item is removed from the basket                         | PASS   |
| Update Item in Basket   | Click 'Update' button           | Item quantity is updated in the basket                  | PASS   |
| Summary total Calculator| Change item quantities         | Total price updates accordingly                         | PASS   |
| Checkout Button         | Click on checkout button        | Redirects to the Stripe checkout page                   | PASS   |
| Checkout validation     | Incomplete checkout submission  | Checkout does not proceed until all fields are filled   | PASS   |
| Checkout Success        | Complete checkout successfully  | Redirects to success page with payment confirmation     | PASS   |
| Checkout Fail           | Attempt failed checkout         | Remains on the same page with error message             | PASS   |
| Order History Update    | Complete checkout and check history | Order appears in order history                        | PASS   |

### Management
| Test                    | Method                         | Expected Outcome                                       | Result |
|-------------------------|--------------------------------|--------------------------------------------------------|--------|
| Management Link         | Access management as admin     | Management link is visible and functional               | PASS   |
| Submit Form             | Add a new product via form     | Product is added and confirmation message displayed     | PASS   |
| Image upload to AWS     | Submit form with image         | Image is stored and displayed correctly via AWS         | PASS   |
| Superuser Access only   | Attempt non-admin access       | Receives "not allowed" message                          | PASS   |
| Product List            | Verify new product appears     | New product is visible with correct details             | PASS   |
| Form Validation         | Submit invalid form data       | Submission is prevented and error messages displayed    | PASS   |

### Product Cards
| Test                    | Method                         | Expected Outcome                                       | Result |
|-------------------------|--------------------------------|--------------------------------------------------------|--------|
| Edit and Delete Buttons | Superuser views product page   | Edit and delete buttons are visible                     | PASS   |
| Edit Button             | Click on edit button           | Redirects to product edit page with a success message   | PASS   |
| Delete Button           | Click on delete button         | Product is removed after confirmation                   | PASS   |
| Wishlist                | Click on wishlist button       | Product is added to wishlist with success message       | PASS   |
| Product Card Image      | Click on product image         | Redirects to product detail page                        | PASS   |

### Product Detail
| Test                    | Method                         | Expected Outcome                                       | Result |
|-------------------------|--------------------------------|--------------------------------------------------------|--------|
| Edit and Delete Buttons | Superuser views product detail | Edit and delete buttons are visible                     | PASS   |
| Edit Button             | Click on edit button           | Redirects to product edit page with a success message   | PASS   |
| Delete Button           | Click on delete button         | Product is removed after confirmation                   | PASS   |
| Wishlist                | Click on wishlist button       | Product is added to wishlist with success message       | PASS   |
| Quantity Adjustment     | Click on + or - buttons        | Quantity increases or decreases correctly               | PASS   |
| Keep Shopping Button    | Click on Keep Shopping button  | Redirects to the products page                          | PASS   |
| Add to Bag Button       | Click on Add to Bag button     | Product is added to bag with success message            | PASS   |
| Add Review              | Submit a review                | Review is added and displayed                           | PASS   |
| Edit Review Button      | Click on edit review button    | Redirects to review edit page                           | PASS   |
| Delete Review Button    | Click on delete review button  | Review is removed                                       | PASS   |
| Edit Review Page        | Submit edited review           | Redirects to product detail page with success message   | PASS   |

### Wishlist 
| Test                    | Method                         | Expected Outcome                                       | Result |
|-------------------------|--------------------------------|--------------------------------------------------------|--------|
| Wishlist Page           | View products on wishlist      | Products are listed correctly on the wishlist page      | PASS   |
| Trash Icon Button       | Click on Trash Icon Button     | Product is removed from the wishlist                   | PASS   |
| Card Image              | Click on Image                 | Redirects to the product detail page                    | PASS   |


