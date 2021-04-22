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
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <a class="navbar-brand" href="#">Lab 7</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
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
  
        <form method="POST" id="registerForm"> 
          <div class="form-group registerform">
            <div class="First"> 
                <label for="username"> Username</label>
                <label for="password"> Password</label>
                <br>
                <input type="text">
                <input type="password">
         
            </div>
            <div> 
                <label for="fullname"> Fullname</label>
                <label for="email"> Email</label>
                <br>
                <input type="text">
                 <input type="email">
                
            </div>
            <label for="location" id="location"> Location</label><br>
            <input type="text">
            <br>

            <label for="biography"> Biography</label><br>
            <textarea type="text" name="biography" class="form-control"></textarea><br>

            <label for="photo">Upload Photo </label>
            <br> 
            <input type="file" name="photo" id="photo" class="form-control" accept="image/*" draggable="true">
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
            let registerform = document.getElementById('registerForm');
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




const Login = {
    name: 'login',
    template: `

    <div class="login-wrap">
	<div class="login-html">
		<h3> Login</3>
		
		<div class="login-form">
			<div class="sign-in-htm">
				<div class="group">
					<label for="user" class="label">Username</label>
					<input id="user" type="text" class="input">
				</div>
				<div class="group">
					<label for="pass" class="label">Password</label>
					<input id="pass" type="password" class="input" data-type="password">
				</div>
				<div class="group">
					<input id="check" type="checkbox" class="check" checked>
					<label for="check"><span class="icon"></span> Keep me Signed in</label>
				</div>
				<div class="group">
					<input type="submit" class="button" value="Sign In">
				</div>
				<div class="hr"></div>
			
			</div>
	
		</div>
	</div>
</div>
 
    `,
    data() {
        return {
            messages: [],
            className: ''
        }
    },

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
    // { path: "/", component: Home },
    { path: "/register", component: Register },
    { path: "/login", component: Login },
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