<script>
	import Title from '../components/Title.svelte';
	import { page } from '$app/stores';
	import '../app.css';
	const routes = [
		{ href: '/dashboard', name: 'Dashboard' },
		{ href: '/sync', name: 'Sync Data' },
		{ href: '/murid', name: 'Murid' },
		{ href: '/logout', name: 'Log Out' }
	];
</script>

<div class="flex h-screen bg-gray-200">
	<div class="p-5 bg-background">
		<Title />
		<!--<h1 class="text-2xl font-bold text-gray-700">Mental Health Dashboard</h1> -->
		<nav>
			<ul>
				{#each routes as route}
					<li class="py-1">
						<a
							href={route.href}
							class:active={$page.url.pathname === route.href}
							class="text-gray-700 hover:text-blue-500 transition duration-200"
						>
							{route.name}
						</a>
					</li>
				{/each}
			</ul>
		</nav>
	</div>
	<main class="flex-1 p-5 overflow-auto bg-green-300">
		<slot />
	</main>
</div>
