# Profile index

Profiles select, constrain, and compose protocol behavior for a named standard
or deployment profile. Packages use `tba-profile-<subject>` names. Protocol wire
implementations remain in layer 50 with `tba-protocol-<subject>` names.

Dependencies flow from profiles to protocols, never from protocols to profiles.
Runtime and application composition may select profiles from this index layer.
