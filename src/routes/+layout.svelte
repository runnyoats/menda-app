<script>
	import Title from '../components/Title.svelte';
	import { page } from '$app/stores';
	import '../app.css';
	import SidebarItem from '../components/SidebarItem.svelte';
	import Modal from 'svelte-simple-modal';
	import Toast from '../components/Toast.svelte';

	const routes = [
		{ href: '/dashboard', name: 'Dashboard' },
		{ href: '/sync', name: 'Sync Data' },
		{ href: '/murid', name: 'Murid' },
		{ href: '/logout', name: 'Log Out' },
		{ href: '/test', name: 'Testing' }
	];
</script>

<div class="flex h-screen bg-gray-200">
	<div class="p-5 bg-background px-5 py-5 z-10 flex flex-col items-center">
		<!--<div class="p-5 bg-background px-5 py-5 z-10">-->
		<Title />
		<nav>
			<ul>
				{#each routes as route}
					<li class="py-1">
						<SidebarItem
							on:clicked={() => {}}
							active={$page.url.pathname === route.href}
							label={route.name}
							href={route.href}
						/>
					</li>
				{/each}
			</ul>
		</nav>
	</div>
	<Modal>
		<Toast />
		<main class="flex-1 p-5 overflow-auto bg-background-secondary">
			<slot />
		</main>
	</Modal>
</div>
