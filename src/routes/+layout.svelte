<script>
	import Title from '../components/Title.svelte';
	import { page } from '$app/stores';
	import '../app.css';
	import SidebarItem from '../components/SidebarItem.svelte';

	const routes = [
		{ href: '/dashboard', name: 'Dashboard' },
		{ href: '/sync', name: 'Sync Data' },
		{ href: '/murid', name: 'Murid' },
		{ href: '/logout', name: 'Log Out' }
	];
</script>

<div class="flex h-screen bg-gray-200">
	<div class="p-5 bg-background px-5 py-5 z-10">
		<Title />
		<!--<h1 class="text-2xl font-bold text-gray-700">Mental Health Dashboard</h1> -->
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
	<main class="flex-1 p-5 overflow-auto bg-background-secondary">
		<slot />
	</main>
</div>
