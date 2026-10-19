<script>
    let { data } = $props();

    let user = $derived(data.user);

    let firstName = $derived(user?.first_name ?? '');
    let lastName = $derived(user?.last_name ?? '');
    let fullName = $derived(
        `${firstName} ${lastName}`.trim() || 'Jobnehmer'
    );

    let initials = $derived(
        `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase() ||
            'U'
    );

    let bio = $derived(
        user?.bio ?? user?.about ?? user?.description ?? ''
    );

    let location = $derived(
        user?.location ?? user?.city ?? ''
    );

    let skills = $derived.by(() => {
        const value = user?.skills;

        if (Array.isArray(value)) {
            return value
                .map((skill) =>
                    typeof skill === 'string' ? skill : skill?.name
                )
                .filter(Boolean);
        }

        if (typeof value === 'string' && value.trim()) {
            return value
                .split(',')
                .map((skill) => skill.trim())
                .filter(Boolean);
        }

        return [];
    });

    let profileFields = $derived([
        firstName,
        lastName,
        user?.email,
        location,
        bio,
        skills.length > 0
    ]);

    let completedFields = $derived(
        profileFields.filter(Boolean).length
    );

    let profileProgress = $derived(
        Math.round((completedFields / profileFields.length) * 100)
    );
</script>