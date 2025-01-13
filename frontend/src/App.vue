<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b">
      <div class="container flex h-14 items-center justify-between">
        <router-link to="/" class="flex items-center">
          <img 
            src="/logo.png" 
            alt="Logo" 
            class="h-12 w-auto"
          />
        </router-link>

        <div class="flex items-center">
          <router-link
            v-if="!authStore.isAuthenticated"
            to="/login"
            class="text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
          >
            Login
          </router-link>
          
          <DropdownMenu v-else>
            <DropdownMenuTrigger>
              <img
                :src="avatarUrl"
                alt="User Avatar"
                class="size-8 rounded-full cursor-pointer hover:opacity-80 transition-opacity"
              />
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" class="w-56">
              <DropdownMenuLabel>Signed in as {{ authStore.user?.name }}</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem @click="router.push('/profile')">
                <User class="mr-2 h-4 w-4" />
                <span>Profile</span>
              </DropdownMenuItem>
              <DropdownMenuItem @click="router.push('/friend-requests')">
                <UserPlus class="mr-2 h-4 w-4" />
                <span>Friend Requests</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem @click="handleLogout">
                <LogOut class="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>
  </div>

  <Toaster richColors />
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { User, UserPlus, LogOut } from 'lucide-vue-next';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { Toaster } from 'vue-sonner';

const authStore = useAuthStore();
const router = useRouter();

const avatarUrl = computed(() => {
  return 'https://ui-avatars.com/api/?name=' + encodeURIComponent(authStore.user?.name || 'User') + '&background=random';
});

const handleLogout = async () => {
  try {
    await authStore.logout(router);
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

onMounted(async () => {
  await authStore.fetchUser();
  if (authStore.isAuthenticated && router.currentRoute.value.meta.requiresGuest) {
    router.push('/profile');
  }
});
</script>

<style scoped>
</style>
