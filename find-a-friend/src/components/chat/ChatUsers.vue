<template>
    <div>
        <div v-for="(friend,id) in friends" :key="id">
            <div>
                {{friend.firstName}}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["friends"]
}
</script>

