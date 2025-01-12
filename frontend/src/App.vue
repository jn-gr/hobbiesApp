<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b">
      <div class="container flex h-14 items-center px-4">
        <router-link to="/" class="flex items-center">
          <img 
            src="/logo.png" 
            alt="Logo" 
            class="h-12 w-auto"
          />
        </router-link>

        <nav class="flex-1 flex justify-center items-center space-x-6 text-sm font-medium">
          <router-link
            to="/"
            class="transition-colors hover:text-primary"
          >
            Home
          </router-link>
          <router-link
            :to="{name: 'Profile Page'}"
            class="transition-colors hover:text-primary"
          >
            Profile
          </router-link>
        </nav>

        <div class="flex items-center space-x-4">
          <router-link
            v-if="!authStore.isAuthenticated"
            to="/login"
            class="text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
          >
            Login
          </router-link>
          <router-link
            v-else
            to="/profile"
            class="text-sm font-medium rounded-full"
          >
            <img
                :src="avatarUrl"
                alt="User Avatar"
                class="size-8 rounded-full"
            />
          </router-link>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const avatarUrl = computed(() => {
  return 'https://ui-avatars.com/api/?name=' + encodeURIComponent(authStore.user?.name || 'User');
});

onMounted(async () => {
  await authStore.fetchUser();
  if (authStore.isAuthenticated && router.currentRoute.value.meta.requiresGuest) {
    router.push('/profile');
  }
});
</script>

<style scoped>
</style>
