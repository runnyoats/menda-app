<script>
	import Button from '../../components/Button.svelte';
</script>

<div class="bg-background rounded-xl p-4 mb-4">
	<p class="text-white font-bold">Export Data</p>
	<p class="text-gray-400 mb-2">Download an Excel copy of all your data saved in MENDA</p>
	<Button>Download Data</Button>
</div>
<div class="bg-background rounded-xl p-4">
	<p class="text-white font-bold">Import Data</p>
	<p class="text-red-400 mb-2">
		Remember to backup your data by exporting first! All data will be replaced!
	</p>
	<div class="flex">
		<Button className="mr-2 overflow-hidden whitespace-nowrap">Select Excel File</Button>
	</div>
</div>

<!--
	<div>
	<div class="flex items-center mb-4">
		<span class="text-gray-400 mr-2">
			<Icon path={mdiInformation} />
		</span>
		<h1 class="font-display text-gray-400 text-lg">click to max</h1>
	</div>
	<div class="bg-background p-2 rounded-xl mb-2">
		<h1 class="font-display text-white text-lg">how to weapon</h1>
	</div>
	<div class="bg-background p-2 rounded-xl mb-2 mt-8">
		<h1 class="font-display text-white text-lg">how to character</h1>
	</div>
</div>
-->
