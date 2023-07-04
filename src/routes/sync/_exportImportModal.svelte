<script>
	import Button from '../../components/Button.svelte';

	let input;
	let files = null;

	function handleFileSelection() {
		if (input) input.click();
	}

	function importData() {
		if (files && files.length > 0) {
			// Handle Excel file here
			// Since Excel file handling is outside the scope of this
			// question, I've left this part blank.
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
</div>
