<script>
	import { mdiInformation } from '@mdi/js';
	import Icon from '../../components/Icon.svelte';
</script>

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
