<script>
	import { onMount } from 'svelte';

	let data = [];

	onMount(async () => {
		const response = await fetch('http://localhost:5000/api/murid_data');
		data = await response.json();
		console.log(data);
		console.log('test');
	});
</script>

<h1>Murid Data</h1>

<table>
	<thead>
		<tr>
			<th>Name</th>
			<th>Class</th>
			<th>Academic Year</th>
			<th>Identity Card Number</th>
		</tr>
	</thead>
	<tbody>
		{#each data as row}
			<tr>
				<td>{row[0]}</td>
				<td>{row[1]}</td>
				<td>{row[2]}</td>
				<td>{row[3]}</td>
			</tr>
		{/each}
	</tbody>
</table>
