# Adware-pr
> Works on python3.7

### Advertiser Webapp

- register new advertiser.
- A seperate webpage as Advertiser DashBoard which allows advertiser
	- to create/remove advertisements (an advertisement form).
	- to check the screen properties on which the particular advertisement is running.
	- to purchase a screen on a rent and adjust the time of display.
	- Option to select from different available geo-location of screens.
	- to purchase a particular subscription , price depends on number of screens and duration.


### Screen Owner Interface

- Register new owner.
- A seperate webpage as Vendor DashBoard which allows vendor
	- check the details of the advertisors on a particular screen.
	- add/delete a screen into his account (a screen registration form).
	- check their earnings from a particular screen and overall.

### Misc

- Calculate total cost to display ad.
- Interactive GUI for geo-location of screens.
- Create Machine Learning models to dynamically predict prices.

### A Layout of Various Forms - 
- Advertiser Registeration and Vendor Registeration
	- (Owner/Advertiser)ID (Auto-Primary Key)
	- Name
	- Email ( or if we remove ID , this can be primary key too.)
	- Mob No.
	- Password
	- Confirm Password

- Advertisement Form
	- AddID(Auto-Primary Key)
	- Advertiser Email(Foreign Key)
	- AddFile
	- CurScreenIDs (can be empty initially).

- Screen Form
	- ScreenID(Auto-Primary Key)
	- VendorEmail(Foreign Key)
	- Address 
	- Price per sec of the add. (to be decided how it will vary n who will set this)
- (Screen , Advertisement)  Table
    - Primary key (screen_id,Ad_id)
    - (screen_id,Ad_id) -> Screen(id) displays ad (Ad_id)

- Toaster Usage
  - toastr.{{message.type}}('{{message}}')
  - where message.type can be info , success , warning , error. 
## API design

- Every registered screen will have a access token to the adware-API.
- API can be accessed by http://127.0.0.1:8000/api?id=SCREEN_TOKEN

### API response object

- Response object is in JSON format.
### JSON attributes
- 'status' is 'ok' if the provided id is correctly sent. else 'not found'
- 'media_path' field contains a list of strings of name of media. The same media name can be used to access the media at http://127.0.0.1:8000/media/media_name
- See vendor-script.py for sample api access code. 
