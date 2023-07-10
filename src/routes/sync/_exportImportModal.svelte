<script>
	import Button from '../../components/Button.svelte';
	import { pushToast } from '../../stores/toast';
	import Icon from '../../components/Icon.svelte';
	import { mdiCheckCircleOutline, mdiLoading } from '@mdi/js';
	import { writable } from 'svelte/store';

	// Create writable stores for isLoading and isSynced
	const isLoading = writable(false);
	const isSynced = writable(false);

	let input;
	let files = null;

	function handleFileSelection() {
		if (input) input.click();
	}

	async function importData() {
		if (files && files.length > 0) {
			const data = new FormData();
			data.append('file', files[0]);

			isLoading.set(true); // Set isLoading to true

			const response = await fetch('http://localhost:3000/import', {
				method: 'POST',
				body: data
			});

			if (response.ok) {
				console.log('Data imported successfully');
				isLoading.set(false); // Set isLoading to false
				isSynced.set(true); // Set isSynced to true
				pushToast('Data imported successfully!');
			} else {
				console.log('Failed to import data');
				isLoading.set(false); // Set isLoading to false
				isSynced.set(false); // Set isSynced to false
				pushToast('Failed to import data.', 'error');
			}
		}
	}

	async function exportData() {
		const response = await fetch('http://localhost:3000/export');
		const blob = await response.blob();
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = 'students_submissions_data.xlsx';
		a.click();
		pushToast('Data exported successfully! Please download the file.');
	}
</script>

<div class="bg-background rounded-xl p-4 mb-4">
	<p class="text-white font-bold">Export Data</p>
	<p class="text-gray-400 mb-2">Download an Excel copy of all your data saved in MENDA</p>
	<Button on:click={exportData}>Download Data</Button>
</div>
<div class="bg-background rounded-xl p-4">
	<p class="text-white font-bold">Import Data</p>
	<p class="text-red-400 mb-2">
		Remember to backup your data by exporting first! All data will be replaced!
	</p>
	<div class="flex">
		<Button className="mr-2" on:click={handleFileSelection}>
			{files !== null && files[0] ? files[0].name : 'Select Excel File'}
		</Button>
		<input bind:this={input} bind:files type="file" accept=".xls,.xlsx" class="hidden" />
		{#if files !== null && files[0]}
			<Button on:click={importData}>Continue</Button>
		{/if}
	</div>
	<p class="text-white mt-4">
		{#if $isLoading || $isSynced}
			Import Status:
			<span class={`font-bold ${$isSynced ? 'text-green-400' : 'text-yellow-400'}`}>
				{#if $isSynced}
					Synced
					<Icon path={mdiCheckCircleOutline} className="text-green-400" />
				{:else}
					Syncing
					<Icon path={mdiLoading} className="text-yellow-400" spin />
				{/if}
			</span>
		{/if}
	</p>
</div>
