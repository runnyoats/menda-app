<script>
	import axios from 'axios';
	import Button from '../../components/Button.svelte';
	import { getContext } from 'svelte';
	import ExportImportModal from './_exportImportModal.svelte';
	import { mdiArrowDown, mdiArrowUp, mdiHelpCircle } from '@mdi/js';
	import Icon from '../../components/Icon.svelte';
	import HowToModal from './SyncHowToModal.svelte';

	const { open: openModal } = getContext('simple-modal');

	function openExportImportModal() {
		openModal(
			ExportImportModal,
			{},
			{
				closeButton: false,
				styleWindow: { background: '#25294A', width: '550px' }
			}
		);
	}

	function openHowTo() {
		openModal(
			HowToModal,
			{},
			{
				closeButton: false,
				styleWindow: { background: '#25294A', width: '1280px' }
			}
		);
	}

	let username = '';
	let password = '';
	let year = new Date().getFullYear();
	const years = Array.from({ length: year - 2019 }, (_, i) => year - i);
	let message = '';
	let dataSynced = false; // new variable to track if data is synced

	async function handleSubmit(event) {
		event.preventDefault();
		try {
			const response = await axios.post('http://localhost:5000/sepkm_scraper', {
				username,
				password,
				year
			});
			console.log(response.data);

			message = `Success: ${response.data.message_student_data}, ${response.data.message_phq9_data}`;
			//dataSynced = true; // set dataSynced to true if successful
			dataSynced = false; // set dataSynced to true if successful
		} catch (error) {
			if (error.response && error.response.data) {
				const errorData = error.response.data;
				message = `Error ${errorData[1]}: ${errorData[0].error}`;
			} else {
				message = error.toString();
			}
			dataSynced = false; // set dataSynced to false if there is an error
		}
	}
</script>

<div class="flex items-center">
	<h1 class="font-display font-black text-4xl text-white text-center md:text-left md:mr-4">
		Synchronize Data
	</h1>
	<Button on:click={openExportImportModal}>Import / Export to Excel</Button>
	<!--<Button on:click={openHowTo}>
		<Icon size={0.8} path={mdiHelpCircle} />
		How to Use
	</Button>-->
</div>

<div class="min-h-screen bg-background-secondary flex items-center justify-center">
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
		<p class="mt-5 text-gray-500 text-center">{message}</p>
		<div class="mt-5 flex space-x-4" />
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
