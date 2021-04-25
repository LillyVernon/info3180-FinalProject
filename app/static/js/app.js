/* Add your Application JavaScript */
// Instantiate our main Vue Instance
const app = Vue.createApp({
    data() {
        return {

        }
    }
});

app.component('app-header', {
    name: 'AppHeader',
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
      <a class="navbar-brand" href="#">United Auto Sales</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
            <router-link  to="/home" class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
        </li>
        <li class="nav-item active">
            <router-link to="/cars" class="nav-link">Add Car</router-link>
        </li>
        <li class="nav-item active">
            <router-link to="/profile" class="nav-link">My Profile</router-link>
        </li>

        </ul>

        <ul class="navbar-nav">

        <li class="nav-item active">
        <router-link to="/register" class="nav-link">Register</router-link>
        </li>
        <li class="nav-item active">
        <router-link to="/auth/login" class="nav-link">Login</router-link>
        </li>

        </ul>

      </div>
    </nav>
    `
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

const Register = {
    name: 'register',
    template: `
    <h1>Registration</h1>
    <div :class="errorclass"> 
        <ul class="uploadmessage" v-for="message in messages">
            <li >{{message}}</li>
        </ul>
    </div>
  
        <form  method="POST" id="registerForm"  @submit.prevent="RegisterUser"> 
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
        RegisterUser() {
            let self = this;
            let registerForm = document.getElementById('registerForm');
            let form_data = new FormData(registerForm)

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


const Cars = {
    name: 'cars',
    template: `
    
    <h1>Add New Car</h1>
    
    <form method="POST" id="carForm" enctype="multipart/form-data" @submit.prevent="RegisterCar">
    <div class="card">
    <div class="row">
    <div class="col-md-6">
        <label>Make</label>
        <input name="make" type="text" class="form-control"/>
    </div>


    <div class="col-md-6">
        <label>Model</label>
        <input  name="model" type="text" class="form-control"/>
    </div>
  </div>


<div class="row">
    <div class="col-md-6">
        <label>Colour</label>
        <input name="colour" type="text" class="form-control"/>
    </div>


    <div class="col-md-6">
        <label>Year</label>
        <input name="year" type="text" class="form-control"/>
    </div>
</div>


<div class="row">
    <div class="col-md-6">
       
        <label>Price</label>
        <input name="price" type="text" class="form-control"/>
    </div>


    <div class="col-md-6">
       
        <label>Car Type</label>
        <input name="car_type" type="text" class="form-control"/>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <label>Transmission</label>
        <input name="transmis" type="text" class="form-control"/>
    </div>
</div>   


<div class="row">
    <div class="col-sm-10">
        
        <label>Description</label>
        <textarea name="desc" type="text" class="form-control"></textarea>
        
</div> 
</div>

<div class="row">
    <div class="col-md-6">
        
            <label> Upload Photo</label>
            <input name="photo" type="file" accept="image/*" class="form-control-file"/>
        </div>
    </div>
    <br>

<div class="col-lg-11">
        <div class="form-group">  
            <button type="submit" class="btn btn-success"> Save</button>
        </div>
        </div>
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
        RegisterCar() {
            let self = this;
            let carForm = document.getElementById('carForm');
            let form_data = new FormData(carForm)

            fetch("/api/cars", {
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

const UploadForm = {
    name: 'upload-form',
    template: `
    <h1>Form</h1>
    <div :class="errorclass">
        <ul class="uploadmessage" v-for="message in messages">
            <li >{{message}}</li>
        </ul>
    </div>
    <form method="POST" id="uploadForm" @submit.prevent="uploadPhoto">
        <div class="form-group">
            <label for="description">Description about Image</label>
            <textarea type="text" name="description" class="form-control"></textarea>
        </div>
        <div class="form-group">
            <label for="photo">Photo Upload</label>
            <input type="file" name="photo" id="photo" class="form-control" accept="image/*" draggable="true">
        </div>
        <button type="submit" class="btn btn-success">Submit</button>
    </form>
    `,
    data() {
        return {
            messages: [],
            className: ''
        }
    },
    methods: {
        uploadPhoto() {
            let self = this;
            let uploadForm = document.getElementById('uploadForm');
            let form_data = new FormData(uploadForm)

            fetch("/api/upload", {
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



const Login = {
    name: 'login',
    template: `
    <div class="login-wrap">
	<div class="login-html">
		<h1> Login</h1>
        <div :class="errorclass"> 
        <ul class="uploadmessage" v-for="message in messages">
            <li >{{message}}</li>
        </ul>
    </div>
		<form  method="POST" id="loginForm"  @submit.prevent="LoginUser"> 
            <div class="login-form lform">
                <div class="sign-in-htm">
                    <div class="group">
                        <label for="username" class="label">Username</label>
                        <input name="username" id="user" type="text" class="input">
                    </div>
                    <div class="group">
                        <label for="password" class="label">Password</label>
                        <input name="password" id="pass" type="password" class="input" data-type="password">
                    </div>
                    <div class="group">
                        <input id="check" type="checkbox" class="check" checked>
                        <label for="check"><span class="icon"></span> Keep me Signed in</label>
                    </div>
                    <br> <br>
                    <div class="group">
                       
                        <button type="submit" class="btn btn-success">Sign In</button>
                    </div>
                    <div class="hr"></div>
                
                </div>
        
            </div>
        </form>
	</div>
</div>
 
    `,
    data() {
        return {
            messages: [],
            className: ''
        }
    },
    methods: {
        LoginUser() {
            let self = this;
            let LoginForm = document.getElementById('loginForm');
            let form_data = new FormData(loginForm)

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
                    if (jsonResponse['successful']) {
                        self.messages = [jsonResponse['successful']['message']];
                        self.className = "successful"
                        router.push('/register')
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


const Home = {
    name: 'home',
    template: `

    <div class="row">
        <div class="column1" style="background-color:#aaa;">
            <h2> BUY AND SELL </h2> 
            <h2> CARS ONLINE </h2>
            <p> United Auto sales provides the fastest, easiest
                    and most friendly way to buy or sell cars online. Find a Great price on the vehicle you want
             <p>

            <span>  
            
                <button type="button" class="btn btn-primary homeregister"> <router-link to="/register" class="homebuttonlinks" >Register</router-link > </button>
                <button type="button" class="btn btn-success homelogin"> <router-link to="/auth/login" class="homebuttonlinks">Login</router-link> </button>
                
            </span>
        </div>


        <div class="column2" style="background-color:#bbb;">
        <img src="./static/homecar.jpg" class="homeimage">
        </div>
  </div>
    `
};

const UserProfile = {
    name: 'userprofile',
    template: `

    <div class="profilecard1">
        <img>
        <h1> Full Name </h1>
        <p> username</p>
        <p>bio</p>

        <p>email</p>
        <p>location</p>
        <p>joined</p>

  </div>
    `
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

// Define Routes
const routes = [
    { path: "/", component: Home },
    { path: "/register", component: Register },
    { path: "/auth/login", component: Login },
    { path: "/cars", component: Cars },
    { path: "/upload", component: UploadForm },
    {
        path: "/users/{user_id}",
        component: UserProfile
    },
    // Put other routes here

    // This is a catch all route in case none of the above matches
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes, // short for `routes: routes`
});

app.use(router);

app.mount('#app');