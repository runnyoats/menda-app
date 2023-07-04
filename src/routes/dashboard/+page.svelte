<script>
	import Button from '../../components/Button.svelte';
</script>

<div class="flex items-center">
	<h1 class="font-display font-black text-4xl text-white text-center md:text-left md:mr-4">
		Power BI Dashboard
	</h1>
	<Button>Export Current Visual</Button>
</div>

<div class="rounded-xl p-4 border border-gray-400 bg-white">
	<div class="relative w-full h-0 overflow-hidden" style="padding-bottom: 50%;">
		<iframe
			class="absolute top-0 left-0 w-full h-full"
			title="menda-dashboard-draft-DB2-3"
			src="https://app.powerbi.com/reportEmbed?reportId=031904be-d4aa-4037-bc6d-e7680756bc57&autoAuth=true&ctid=0ad0fbf8-69ca-4e5e-afad-cd70424ac626"
			frameborder="0"
			allowFullScreen="true"
		/>
	</div>
</div>
