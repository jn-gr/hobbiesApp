<template>
  <div class="container mt-5">
    <div v-if="isLoggedIn">
      <h1 class="mb-4">Profile</h1>

      <form @submit.prevent="submitUpdateProfile" class="mb-5">
        <div class="mb-3">
          <label for="name" class="form-label">Name:</label>
          <input
            type="text"
            id="name"
            class="form-control"
            v-model="formData.name"
          />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input
            type="email"
            id="email"
            class="form-control"
            v-model="formData.email"
          />
        </div>

        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth:</label>
          <input
            type="date"
            id="dob"
            class="form-control"
            v-model="formData.date_of_birth"
          />
        </div>

        <div class="mb-3">
          <label for="hobbies" class="form-label">Hobbies:</label>
          <select
            id="hobbies"
            class="form-select"
            multiple
            v-model="formData.hobbies"
          >
            <option v-for="hobby in hobbies" :key="hobby.id" :value="hobby.id">
              {{ hobby.name }}
            </option>
          </select>
          <small class="text-muted"
            >Hold Ctrl or Cmd to select multiple options.</small
          >
        </div>

        <button type="submit" class="btn btn-primary">Update Profile</button>
      </form>

      <h2 class="mb-4">Change Password</h2>
      <form @submit.prevent="submitUpdatePassword">
        <div class="mb-3">
          <label for="oldPassword" class="form-label">Old Password:</label>
          <input
            type="password"
            id="oldPassword"
            class="form-control"
            v-model="passwordData.oldPassword"
          />
        </div>

        <div class="mb-3">
          <label for="newPassword" class="form-label">New Password:</label>
          <input
            type="password"
            id="newPassword"
            class="form-control"
            v-model="passwordData.newPassword"
          />
        </div>

        <div class="mb-3">
          <label for="confirmPassword" class="form-label">Confirm Password:</label>
          <input
            type="password"
            id="confirmPassword"
            class="form-control"
            v-model="passwordData.confirmPassword"
          />
        </div>

        <button type="submit" class="btn btn-danger">Change Password</button>
      </form>
    </div>

    <!-- Not logged in message -->
    <div v-else class="text-center mt-5">
      <p class="lead">
        Currently you are not signed in. To view your profile page, please login.
      </p>
      <button class="btn btn-primary" @click="goToSignin">Go to Sign In</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { User, Hobby } from "../types";

export default defineComponent({
  name: "Profile",
  setup() {
    const router = useRouter();

    // State for login check, hobbies, and user data
    const isLoggedIn = ref(false);
    const hobbies = ref<Hobby[]>([]);
    const formData = reactive<User>({
      id: 0,
      name: "",
      email: "",
      date_of_birth: "",
      hobbies: [],
    });

    // State for password change
    const passwordData = reactive({
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
    });

    // Fetch hobbies from the server
    const fetchHobbies = async () => {
      try {
        const response = await fetch("/api/hobbies/");
        if (!response.ok) throw new Error("Failed to fetch hobbies");
        hobbies.value = await response.json();
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    };

    // Fetch user profile data from the server
    const fetchUserProfile = async () => {
      try {
        const response = await fetch("/api/profile/");
        if (response.ok) {
          const userData: User = await response.json();
          Object.assign(formData, userData);
          isLoggedIn.value = true;
        } else if (response.status === 401) {
          isLoggedIn.value = false; // User is not authenticated
        } else {
          throw new Error("Failed to fetch user profile");
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    };

    // Submit profile update
    const submitUpdateProfile = async () => {
      try {
        const response = await fetch("/api/profile/update/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.errors);
        alert("Profile updated successfully.");
      } catch (error) {
        console.error("Error updating profile:", error);
        alert("Failed to update profile. Please check your input.");
      }
    };

    // Submit password update
    const submitUpdatePassword = async () => {
      try {
        const response = await fetch("/api/profile/password/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(passwordData),
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.errors);
        alert("Password updated successfully.");
        passwordData.oldPassword = "";
        passwordData.newPassword = "";
        passwordData.confirmPassword = "";
      } catch (error) {
        console.error("Error updating password:", error);
        alert("Failed to update password. Please check your input.");
      }
    };

    // Navigate to the signin page
    const goToSignin = () => {
      router.push("/signin");
    };

    // On component mount
    onMounted(() => {
      fetchHobbies();
      fetchUserProfile();
    });

    return {
      isLoggedIn,
      formData,
      passwordData,
      hobbies,
      submitUpdateProfile,
      submitUpdatePassword,
      goToSignin,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
