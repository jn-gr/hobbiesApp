<template>
  <div class="container mt-5">
    <h1 class="mb-4">Profile</h1>

    <form @submit.prevent="updateProfile" class="mb-5">
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
        <small class="text-muted">Hold Ctrl or Cmd to select multiple options.</small>
      </div>

      <button type="submit" class="btn btn-primary">Update Profile</button>
    </form>

    <h2 class="mb-4">Change Password</h2>
    <form @submit.prevent="updatePassword">
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
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from "vue";
import { User, Hobby } from "../types";

export default defineComponent({
  name: "Profile",
  setup() {
    // State for hobbies and user data
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
        alert("Unable to load hobbies. Please try again later.");
      }
    };

    // Fetch user profile data from the server
    const fetchUserProfile = async () => {
      try {
        const response = await fetch("/api/profile/");
        if (!response.ok) throw new Error("Failed to fetch user profile");
        const userData: User = await response.json();
        Object.assign(formData, userData);
      } catch (error) {
        console.error("Error fetching user profile:", error);
        alert("Unable to load profile. Please try again later.");
      }
    };

    // Update profile
    const updateProfile = async () => {
      try {
        const response = await fetch("/api/profile/update/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
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

    // Update password
    const updatePassword = async () => {
      try {
        const response = await fetch("/api/profile/password/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify(passwordData),
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.errors);
        alert("Password updated successfully.");
        // Optionally, clear the password form
        passwordData.oldPassword = "";
        passwordData.newPassword = "";
        passwordData.confirmPassword = "";
      } catch (error) {
        console.error("Error updating password:", error);
        alert("Failed to update password. Please check your input.");
      }
    };

    // Utility to get CSRF token
    const getCsrfToken = (): string => {
      const token = document.querySelector<HTMLMetaElement>(
        'meta[name="csrf-token"]'
      )?.content;
      return token || "";
    };

    // On component mount
    onMounted(() => {
      fetchHobbies();
      fetchUserProfile();
    });

    return {
      formData,
      passwordData,
      hobbies,
      updateProfile,
      updatePassword,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
