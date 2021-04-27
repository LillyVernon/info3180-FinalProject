const app = Vue.createApp({
    data() {
        return {

        }
    }
});

app.component('app-header', {
    name: 'AppHeader',
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <a class="navbar-brand" href="#">United Auto Sales</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          
          <li  v-if="user_logged_in" class="nav-item active">
          <router-link class="nav-link" to="/cars/new"> Add Car <span class="sr-only">(current)</span></router-link>
        </li>
          <li v-if="user_logged_in" class="nav-item active">
          <router-link class="nav-link" to="/explore"> Explore <span class="sr-only">(current)</span></router-link>
        </li>
        <li v-if="user_logged_in" class="nav-item active">
        <router-link class="nav-link" @click="profile()" v-bind:to="'/users/' + loggedinUser">My Profile <span class="sr-only">(current)</span></router-link>
      
        </ul>

        <ul class="navbar-nav">
        <li v-if="user_logged_in" class="nav-item active">
            <router-link class="nav-link" to="/login">Login <span class="sr-only">(current)</span></router-link>
          </li>
          <li  v-if="user_logged_in" class="nav-item active">
            <router-link class="nav-link" to="/register"> Register <span class="sr-only">(current)</span></router-link>
          </li>

        </li>
          <li v-if="user_logged_in" class="nav-item active">
            <router-link class="nav-link" to="/logout">Logout <span class="sr-only">(current)</span></router-link>
          </li>

        </ul>
      </div>
    </nav>
    `,

    computed: {
        user_logged_in: function() {
            if (sessionStorage.getItem('token')) {
                return true;
            } else {
                return false;
            }
        }
    },

    methods: {
        profile: function() {
            let self = this;
            this.$router.push("/users/" + self.loggedinUser)
            location.reload();
        }
    },

    data: function() {
        return {
            loggedinUser: 0
        }
    },

    created: function() {
        let self = this;
        fetch('/api/secure', {
                'headers': {
                    'Authorization': 'Bearer ' + sessionStorage.getItem('token')
                }
            }).then(function(response) {
                return response.json();
            }).then(function(response) {
                let result = response.data;
                self.loggedinUser = result.user.userid;
            })
            .catch(function(error) {
                console.log(error);
            });
    }
});

app.component('app-footer', {
    name: 'AppFooter',
    template: `
      <footer>
           <div class="container">
                 <p>Copyright &copy; {{ year }} Flask Inc.</p>
             </div>
        </footer>
         `,
    data() {
        return {
            year: (new Date).getFullYear()
        }
    }
});

const Home = {
    name: 'Home',
    template: `
    

    
    <div class="row">
        <div class="column1">
        <div class="para">
            <h2> BUY AND SELL </h2> 
            <h2> CARS ONLINE </h2>
            <p> United Auto sales provides the fastest, easiest
            and most friendly way to buy or sell cars online. Find a Great price on the vehicle you want
             </p>
             </div>

            <span>  
            
            <button id="regbtn" @click="$router.push('register')" type="button" class="btn btn-success">Register</button>
            <button id="loginbtn" @click="$router.push('login')" type="button" class="btn btn-primary">Login</button>
                
                
            </span>
        </div>


        <div class="column2">
        <img src="./static/homecar.jpg" class="homeimage">
        </div>
  </div>
    `,
    data() {
        return {}
    }
};


const NotFound = {
    name: 'NotFound',
    template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
    data() {
        return {}
    }
};

const Login = {
    name: "login",
    data() {
        return {

            displayFlash: false,
            errormessage: "",

        }
    },

    template: `
    <div class = 'login-container'>
        <h2> Login to your account </h2>
 
    
        <form v-on:submit.prevent="loginUser" method="POST" enctype="multipart/form-data" id="loginForm">
        <div class="card">
            <div class = "form-group">
                <label> Username </label><br>
                <input type="text" name="username" class="form-control"><br>
                <label> Password </label><br>
                <input type="password" name="password" class="form-control"><br>
                <button class="btn btn-success" > Login </button>
            </div>
                
            </div> 
        </form>
    </div>
    <div class="alert alert-danger" v-if="isError">
    <ul>
        <li v-for="error in errors">{{ error }}</li>
    </ul>
</div>
    `,
    data: function() {
        return {
            token: '',
            errors: [],
            isError: false
        }
    },
    methods: {
        loginUser() {
            let self = this;
            let loginForm = document.getElementById('loginForm');
            let form_data = new FormData(loginForm);
            fetch("/api/auth/login", {
                    method: 'POST',
                    body: form_data,
                    headers: {
                        'X-CSRFToken': token
                    },
                    credentials: 'same-origin'
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {
                    console.log(jsonResponse)

                    if (typeof jsonResponse.data === 'undefined') {
                        console.log(jsonResponse.message);
                        self.isError = true;
                        self.errors = [jsonResponse.message];

                    }
                    if (jsonResponse.errors) {
                        self.isError = true;
                        self.isSuccess = false;
                        self.errors = jsonResponse.errors;
                    } else {
                        console.log(jsonResponse.message);
                        let tkn_jwt = jsonResponse.data.token;
                        sessionStorage.setItem('token', tkn_jwt);
                        console.info('Token stored in sessionStorage.');
                        self.token = tkn_jwt;
                        router.push("/explore")
                    }

                })
                .catch(function(error) {
                    console.log(error);
                });

        }

    },

};

const Logout = {
    name: "logout",
    template: `
        <div>Logging out...</div>
    
    `,

    methods: {
        logOut: function() {
            let self = this;
            fetch("/api/auth/logout", { method: 'POST', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token } })
                .then(function(response) {
                    return response.json();
                })
                .then(function(response) {
                    let result = response.data;
                    sessionStorage.removeItem('token');
                    router.push("/")

                })
                .catch(function(error) {
                    console.log(error);
                })
        }
    },

    beforeMount() {
        this.logOut()
    }
};

const Register = {
    name: 'register',
    template: `
    <h1>Registration</h1>
    <div :class="errorclass"> 
        <ul class="uploadmessage" v-for="message in messages">
            <li >{{message}}</li>
        </ul>
    </div>
  
        <form  method="POST" id="registerForm"  @submit.prevent="registerMethod"> 
          <div class="form-group registerform">
            <div class="First"> 
                <label for="username"> Username</label>
                <label for="password"> Password</label>
                <br>
                <input name="username" type="text">
                <input name="password" type="password">
         
            </div>
            <div> 
                <label for="fullname"> Fullname</label>
                <label for="email"> Email</label>
                <br>
                <input name="fullname" type="text" class="form-control">
                <input name="email" type="email" class="form-control">
                
            </div>
            <label for="location" id="location"> Location</label><br>
            <input name="location" type="text">
            <br>
            <label for="biography"> Biography</label><br>
            <textarea type="text" name="biography" class="form-control"></textarea><br>
            <label for="photo">Upload Photo </label>
            <br> 
            <input type="file" name="photo" id="photo" class="form-control" accept="image/*" draggable="true">
            <br> 
            <br>
            <br>
            <button type="submit" class="btn btn-success">Submit</button>
        </div>
            </form>
    `,
    data() {
        return {
            messages: [],
            className: ''
        }
    },
    methods: {
        registerMethod() {
            let self = this;
            let uploadForm = document.getElementById('registerForm');
            let form_data = new FormData(uploadForm)

            fetch("/api/register", {
                    method: 'POST',
                    body: form_data,
                    headers: {
                        'X-CSRFToken': token
                    },
                    credentials: 'same-origin'
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {
                    if (jsonResponse['successful']) {
                        self.messages = [jsonResponse['successful']['message']];
                        self.className = "successful"
                    } else {
                        self.messages = jsonResponse['errors']['errors'];
                        self.className = "errors"
                    }

                })
                .catch(function(error) {
                    console.log(error);
                });

        }
    }
};



const CarForm = {
    name: "car-form",
    data() {
        return {
            isSuccessUpload: false,
            displayFlash: false,
            successmessage: "",
            errormessage: "",
        }
    },

    template: `
     <div class = 'addcar-container'>
         <h2> Add New Car </h2>
 

         <div class="alert alert-danger" v-if="isError">
                 <ul>
                     <li v-for="error in errors">{{ error }}</li>
                 </ul>
         </div>
     
     
         <form v-on:submit.prevent="registerCar" method="POST" enctype="multipart/form-data" id="carForm">
         <div  class="card">
             <div class="form-group">
 
                 <div class = "row">
                     <div class = "col-md-6">
                         <label> Make </label><br>
                         <input type="text" class="form-control" name="make"><br>
                     </div>
 
                     <div class = "col-md-6">
                         <label> Model </label><br>
                         <input type="text" class="form-control" name="model"><br>
                     </div>
                 </div>
 
                 <div class = "row">
                     <div class = "col-md-6">
                         <label> Colour </label><br>
                         <input type="text" class="form-control" name="colour"><br>
                     </div>
 
                     <div class = "col-md-6">
                         <label> Year </label><br>
                         <input type="text" class="form-control" name="year"><br>
                     </div>
                 </div>
 
                 <label> Price </label><br>
                 <input type="text" class="form-control" name="price"><br>
 
                 <div class = "row">
                     <div class="col-md-6">
                         <label for="car_type"> Car Type </label><br>
                         <select name="car_type" class="form-control" id="car_type"> 
                            <option>SUV</option>
                            <option>Lexus</option>
                            <option>Lamborghini</option>
                         </select><br>
                     </div>
 
             
                     <div class = "col-md-6">
                         <label> Transmission </label><br>
                         <select name="transmission" class="form-control"> 
                             <option value=Automatic> Automatic </option>
                             <option value=Manual> Manual </option>
 
                         </select><br>
                     </div>
                 </div>
 
                 <label> Description </label><br>
                 <textarea name="description" class="form-control"> </textarea><br>
 
                 <label> Upload Photo: </label><br>
                 <input type="file" name="photo">
 
             </div>
             <div class = "carbtn">
                 <button class="btn btn-success" > Add New Car </button>
             </div>
         </div>
         </form>
     </div>
<div class="alert alert-success" v-if="isSuccess">
     <p v-for="success in successMessage">{{ success }}</p>
</div>

     `,

    data: function() {
        return {
            errors: [],
            successMessage: [],
            isSuccess: false,
            isError: false
        };
    },


    methods: {
        registerCar() {
            let self = this;
            let carForm = document.getElementById('carForm');
            let form_data = new FormData(carForm);
            fetch("/api/cars", {
                    method: 'POST',
                    body: form_data,
                    headers: {
                        'Authorization': 'Bearer ' + sessionStorage.getItem('token'),
                        'X-CSRFToken': token
                    },
                    credentials: 'same-origin'

                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {

                    console.log(jsonResponse);

                    if (jsonResponse.errors) {
                        self.isError = true;
                        self.isSuccess = false;
                        self.errors = jsonResponse.errors;
                    } else if (jsonResponse.success) {
                        self.isError = false;
                        self.isSuccess = true;
                        self.successMessage = jsonResponse.success;

                    }
                })
                .catch(function(error) {
                    console.log(error);
                });

        }

    },

};

const Explore = {
    name: "explore",

    template: `
    <div>
        <div class = "exp-container">
            <h2> Explore </h2><br>
            
        
            <form v-on:submit.prevent="exploreSearch" method="GET" enctype="multipart/form-data" id="searchForm">
            <div class = "exp-card">
                <div class="form-group">
                    <div class = "form-row">
                        <div class = "col">
                            <label class = "mm"> Make </label><br>
                            <input type="text" class = "form-control" name="searchbymake" v-model="searchMake"><br>
                        </div>
                        <div class = "col">
                            <label class = "mm"> Model </label><br>
                            <input type="text" class = "form-control" name="searchbymodel" v-model="searchModel"><br>
                        </div>
                        <div class = "exp-btn">
                        <button class="btn btn-success" > Search </button>
                        </div>
                    
                    </div>
                    <br>
                    
                    
                </div>
            </div>
            </form>
            </div>

            <ul class="explist">    
            <li v-for="car in allcars">

        <div class="cars-group "> 
                <div class="card-car ">
                    <img class="single img-top" id="car_img" :src="'/static/uploads/'  + car.photo" alt="car img">
                    <div class = "card-body">
                        <div class = "car-title">
                            <h6 id="titles">{{car.year}} {{car.make}} </h6>
                            <span id="price1" class="price-tag"> $ {{car.price}} </span>
                        </div>
                        <p class="car-text"> {{car.model}} </p>
                        <button @click="carinfo(car.id)" class="btn btn-dark btn-block"> View More Details </button>
                    </div>
                </div> 
        </div>

                
            </li>
            </ul>
             
    </div>
    
    `,
    data: function() {
        return {
            allcars: [],
            userid: 0,
            searchMake: '',
            searchModel: ''
        }
    },

    methods: {
        exploreSearch() {
            let self = this;
            fetch('/api/search?searchbymake=' + self.searchMake + '&searchbymodel=' + self.searchModel, {
                    method: 'GET',
                    headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {
                    self.allcars = jsonResponse.searchedcars
                    console.log(jsonResponse);
                })
                .catch(function(error) {
                    //this.errormessage = "Something went wrong"
                    console.log(error);
                });

        },

        pagestart: function() {
            let self = this;
            fetch("/api/cars", { method: 'GET', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') } })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {
                    // display a success message
                    self.allcars = jsonResponse.allcars.slice(-3);
                    console.log(jsonResponse.allcars.slice(-3));
                    console.log(jsonResponse.allcars);

                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        carinfo: function(car_id) {
            this.$router.push("/cars/" + car_id)

        },


    },
    created: function() {
        this.pagestart();
    }
};

const Cardetails = {
    name: "carinfo",
    props: ['car_id'],
    template: `
    <div class ="rrow">
        <div class = "ccolumn">
        <img id="car_img" :src="'/static/uploads/' + photo" alt="car img" class="cardimg">
        </div>
        <div class = "cccolumn">

                <div class = "yearmake">
                    <h3 class = "card-title">  {{ year }}  {{ make }} </h3> <br>
                    <p class="model"> {{model}} </p>

                    <p> {{description}} </p> 
                </div>



                <div class = "cinfobody">
                    <label>Colour</label>
                    <p class="card-text"> {{colour}} </p>

                    <label>Body Type</label>
                    <p class="card-text"> {{car_type}} </p> 

                    <label>Price</label>
                    <p class="card-text"> {{price}} </p> 

                    <label>Transmission</label>
                    <p class="card-text"> {{transmission}} </p> 

                    <div class = "carinfobtns">
                        <button class="btn btn-success" > Email Owner </button>
                        <button v-if="faved" type="button" class="btn btn-default btn-circle">
                           Add to Favourites
                        </button>
                        <button v-else" @click="favouritecar(car_id)" type = "button" class="btn btn-default btn-circle" style="background-color: blue; color: white" >    
                        Add to Favorites!  
                        </button>
                    </div>

                </div>
            </div>
        </div>
    </div>
    
    `,
    data: function() {
        return {

            year: "",
            price: 0,
            model: "",
            description: "",
            colour: "",
            transmission: "",
            make: "",
            car_type: "",
            photo: "",
            favorite: false



        }
    },
    created: function() {
        let self = this;
        this.viewCarinfo(self.car_id);
    },

    methods: {
        viewCarinfo(car_id) {
            let self = this;
            fetch('/api/cars/' + car_id, {
                    method: 'GET',
                    headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {
                    self.year = jsonResponse.year;
                    self.model = jsonResponse.model;
                    self.make = jsonResponse.make;
                    self.description = jsonResponse.description;
                    self.colour = jsonResponse.colour;
                    self.transmission = jsonResponse.transmission;
                    self.photo = jsonResponse.photo;
                    self.car_type = jsonResponse.car_type;
                    self.price = jsonResponse.price;
                    self.favorite = jsonResponse.Faved;
                    console.log(jsonResponse);


                })
                .catch(function(error) {
                    console.log(error);
                });

        },
        favouritecar: function(car_id) {
            fetch("/api/cars/" + car_id + "/favourite", { method: 'POST', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }, credentials: 'same-origin' })
                .then(function(response) {
                    return response.json();
                }).then(function(jsonResponse) {
                    console.log(jsonResponse.message);
                    location.reload()
                }).catch(function(error) {
                    console.log(error);
                });
        },


    },

};

const UserProfile = {
    name: "userprofile",
    props: ['user_id'],
    template: `

    <div class="profcard">
    <div class="row">
        <div class = "person-img col-3"  v-if="user !==null">
            <img v-bind:src="'/static/uploads/' + user.photo" / class="profpic"> 
        </div>

        <div class="profilecard-body col-6"  v-if="user !==null">
        <h1 class = "uname"> {{user.name}}</h1> 
        <p class = "usname">@{{user.username}} </p>
        <p class = "bio">{{user.biography}} </p>
        <div class = "biospaced">
        <p class = "bio">Email </p> {{user.email}}
        <p class = "bio">Location </p>{{user.location}}
        <p class = "bio">Joined</p> {{user.date_joined}}
        </div>
        </div>
    </div>
</div>
        <br><br>
        <h2 > Cars Favourited </h2>
    
        <ul class="explist">    
        <li v-for="car in allcars">

    <div class="cars-group "> 
            <div class="card-car ">
                <img class="single img-top" id="car_img" :src="'/static/uploads/'  + car.photo" alt="car img">
                <div class = "card-body">
                    <div class = "car-title">
                        <h6 id="titles">{{car.year}} {{car.make}} </h6>
                        <span id="price1" class="price-tag"> $ {{car.price}} </span>
                    </div>
                    <p class="car-text"> {{car.model}} </p>
                    <button @click="carinfo(car.id)" class="btn btn-dark btn-block"> View More Details </button>
                </div>
            </div> 
    </div>

            
        </li>
        </ul>
    
        </div>
        `,
    data: function() {
        return {
            allcars: [],
            user: {}
        }
    },
    created: function() {
        let self = this;
        this.viewUserinfo(self.user_id);
        this.carsfavourited(self.user_id);
    },

    methods: {
        viewUserinfo(user_id) {
            let self = this;
            fetch('/api/users/' + user_id, {
                    method: 'GET',
                    headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(jsonResponse) {
                    self.user = jsonResponse.user;
                })
                .catch(function(error) {
                    //this.errormessage = "Something went wrong"
                    console.log(error);
                });

        },
        carsfavourited: function(user_id) {
            let self = this;
            fetch("/api/users/" + user_id + "/favourites", { method: 'GET', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }, credentials: 'same-origin' })
                .then(function(response) {
                    return response.json();
                }).then(function(jsonResponse) {
                    // display a success message
                    self.allcars = jsonResponse.favouritecars
                    console.log(jsonResponse);
                }).catch(function(error) {
                    console.log(error);
                });
        },
        carinfo: function(car_id) {
            this.$router.push("/cars/" + car_id)

        },


    },

};









// Define Routes
const routes = [
    { path: "/", component: Home },
    { path: "/register", component: Register },
    { path: "/login", component: Login },
    { path: "/cars/new", component: CarForm },
    { path: "/explore", component: Explore },
    { path: "/cars/:car_id", component: Cardetails, props: true },
    { path: "/logout", component: Logout },
    { path: "/users/:user_id", component: UserProfile, props: true },




    // Put other routes here

    // This is a catch all route in case none of the above matches
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes, // short for `routes: routes`
});

app.use(router);

app.mount('#app')