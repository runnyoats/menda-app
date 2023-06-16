<script>
	import axios from 'axios';

	let username = '';
	let password = '';
	let year = new Date().getFullYear();
	const years = Array.from({ length: year - 2019 }, (_, i) => year - i);

	async function handleSubmit(event) {
		event.preventDefault(); // prevent the form from submitting normally
		const response = await axios.post('http://localhost:5000/api', {
			username,
			password,
			year // include year data
		});
		console.log(response.data);
	}
</script>

<div class="min-h-screen bg-gray-100 flex items-center justify-center">
	<div class="bg-white p-10 rounded-lg shadow-md w-80">
		<h2 class="text-2xl font-bold mb-10 text-gray-800 text-center">Sync Data</h2>
		<form on:submit={handleSubmit}>
			<div class="space-y-5">
				<div>
					<label for="username" class="block text-sm font-medium text-gray-700">Username</label>
					<input
						id="username"
						type="text"
						bind:value={username}
						required
						class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
					/>
				</div>
				<div>
					<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						required
						class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
					/>
				</div>
				<div>
					<label for="year" class="block text-sm font-medium text-gray-700">Year</label>
					<select
						id="year"
						bind:value={year}
						class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
					>
						{#each years as yearOption}
							<option value={yearOption}>{yearOption}</option>
						{/each}
					</select>
				</div>
				<div>
					<button
						type="submit"
						class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
						>Sync</button
					>
				</div>
			</div>
		</form>
	</div>
</div>

<style lang="postcss">
	.hovered {
		@apply text-white !important;
		@apply bg-primary;
	}

	.options {
		max-height: calc(50vh);
		overflow-y: auto;
	}
</style>
