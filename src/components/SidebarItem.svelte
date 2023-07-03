<script>
	import { createEventDispatcher } from 'svelte';

	export let label;
	export let href;
	export let active;

	const dispatch = createEventDispatcher();

	function clicked() {
		dispatch('clicked');
	}
</script>

<a
	on:click={clicked}
	class={`flex items-center w-full rounded-xl p-2 ease-in duration-150 ${active ? 'active' : ''}`}
	{href}
>
	<div class="group py-2 flex items-center px-4 cursor-pointer transition-colors">
		<span
			class="font-body font-semibold text-lg leading-none text-gray-500 group-hover:text-white ease-in duration-150 {active
				? 'active'
				: ''}"
		>
			{label}
		</span>
	</div>
</a>

<style lang="postcss">
	.active {
		@apply text-white;
		@apply bg-primary;
	}
</style>
