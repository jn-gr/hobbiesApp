<template>
    <div class="login">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
            <div>
                <label>Email</label>
                <input type="email" v-model="form.email" required>

            </div>

            <div>
                <label>Password:</label>
                <input type="password" v-model="form.password" required>

            </div>
            <button type="submit">Login</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>


    </div>
</template>

<script>
export default {
    data() {
        return {
            form: {
                email: "", 
                password: "",

            },
            errorMessage: ""
        };
    },
    methods: {
        async handleLogin() {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/login/", {
            method: "POST", 
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(this.form)
        });

        const data = await response.json();
        if (data.success) {
            this.errorMessage = "";
            this.$router.push("/profile");
        } else {
            this.errorMessage = data.message;
        }
    } catch (error) {
        this.errorMessage = "An error has occurred.";
    }
},
    },
};
</script>