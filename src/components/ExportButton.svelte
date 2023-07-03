<script>
	import Button from './Button.svelte';

	function handleExport() {
		// This is where you'd add the code to export to CSV.
		// For now, it's just showing an alert.
		alert('Export button clicked!');
	}
</script>

<Button on:click={handleExport} color="blue" size="md">Export to CSV</Button>
