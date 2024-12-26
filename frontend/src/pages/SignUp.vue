<template>
    <div class="signup">
        <h1>Sign Up</h1>
        <form @submit.prevent="handleSignup">
            <div>
                <label>Name:</label>
                <input type="text" v-model="form.name" required>
            </div>

            <div>
                <label>Email:</label>
                <input type="email" v-model="form.email" required>

            </div>

            <div>
                <label>Password:</label>
                <input type="password" v-model="form.password" required>
            </div>

            <div>
                <label>Select or Add Hobbies:</label>
                <select v-model="selectedHobbies" multiple style="min-width: 50px;">
                    <option v-for="hobby in availableHobbies" :key="hobby.id" :value="hobby.name">
                        {{ hobby.name }}
                    </option>
                </select>
                <input type="text" v-model="newHobby" placeholder="Add a new hobby">
                <button type="button" @click="addNewHobby">Add Hobby</button>
            </div>

            <button type="submit">Sign Up</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </form>

    </div>
</template>


<script>
export default {
    data() {
        return {
            form: {
                name: "",
                email: "",
                password: "",
            },
            selectedHobbies: [], // Bind selected hobbies
            availableHobbies: [], // Fetch available hobbies from backend
            newHobby: "", // To add new hobbies
            errorMessage: "",
            successMessage: "",
        };
    },
    methods: {
        async fetchAvailableHobbies() {
            const response = await fetch("http://127.0.0.1:8000/api/hobbies/");
            if (response.ok) {
                this.availableHobbies = await response.json();
            }
        },
        async handleSignup() {
            try {
                const response = await fetch("http://127.0.0.1:8000/api/signup/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: this.form.name,
                        email: this.form.email,
                        password: this.form.password,
                        hobbies: this.selectedHobbies, 
                    }),
                });

                const data = await response.json();
                console.log("Signup Response:", data);

                if (data.success) {
                    this.successMessage = data.message;
                    this.errorMessage = "";
                    setTimeout(() => this.$router.push("/login"), 2000);
                } else {
                    this.errorMessage = data.message || "Signup failed.";
                    this.successMessage = "";
                }
            } catch (error) {
                console.error("Error during signup:", error);
                this.errorMessage = "An error has occurred.";
            }
        },
        async addHobby(newHobby) {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/hobbies/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newHobby }),
        });

        const data = await response.json();
        if (response.ok) {
            this.hobbies.push(data); // Add the new hobby to the dropdown options
        } else {
            console.error("Error adding hobby:", data.message);
        }
    } catch (error) {
        console.error("Error adding hobby:", error);
    }
},

    },
    mounted() {
        this.fetchAvailableHobbies();
    },
};
</script>