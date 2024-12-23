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

interface Hobby {
  id: number;
  name: string;
}

interface User {
  id: number;
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: number[];
}

export default defineComponent({
  name: "Profile",
  setup() {
    const router = useRouter();

    const isLoggedIn = ref(false);
    const hobbies = ref<Hobby[]>([]);
    const formData = reactive<User>({
      id: 0,
      name: "",
      email: "",
      date_of_birth: "",
      hobbies: [],
    });

    const passwordData = reactive({
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
    });

    const fetchHobbies = async (): Promise<void> => {
      const response = await fetch("/api/hobbies/");
      if (response.ok) {
        hobbies.value = await response.json();
      }
    };

    const fetchUserProfile = async (): Promise<void> => {
      const response = await fetch("/api/profile/");
      if (response.ok) {
        const userData: User = await response.json();
        Object.assign(formData, userData);
        isLoggedIn.value = true;
      } else if (response.status === 401) {
        isLoggedIn.value = false;
      }
    };

    const submitUpdateProfile = async (): Promise<void> => {
      const response = await fetch("/api/profile/update/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      if (result.success) {
        Object.assign(formData, result.data);
        alert(result.message);
      }
    };

    const submitUpdatePassword = async (): Promise<void> => {
      const response = await fetch("/api/profile/password/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(passwordData),
      });
      const result = await response.json();
      if (result.success) {
        alert(result.message);
        passwordData.oldPassword = "";
        passwordData.newPassword = "";
        passwordData.confirmPassword = "";
      }
    };

    const goToSignin = (): void => {
      router.push("/signin");
    };

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
