<script>
	import { getData } from '$lib/fetcher.js';

	const response = getData('http://localhost:5000/api/get-char/BewareStormisComming');
</script>

{#await $response}
	<p>Loading...</p>
{:then data}
	<ul>
		<li>Name: {data.name}</li>
		<li>POB: <input type="text" value={data.pob} /></li>
	</ul>
{:catch}
	<p>There was an error</p>
{/await}
