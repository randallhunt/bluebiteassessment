# Assessment Notes

## General notes

- I didn't track my time, largely because I had a lot of other things going on this week and couldn't guarantee an uninterrupted block of time to dedicate to work I'm not getting paid for. So I did this bit by bit as free time permitted
- The project instructions were very vague, and would be reflective of the kind of thing where, in an actual work situation, I would spend a lot more time having conversations and getting clarification
- In particular, one place where the vagueness really became an impediment was in "part 3: advanced filtering", because as I can best understand there are only text and numeric data, but the instructions seem to imply that others would be possible
- With "Part 3" so unclear, I decided that this was a good place to stop and we can talk about it when we meet, if desired. I will also make notes below about how I might have proceeded if I had more time to waste and/or the instructions had been more clear about specific desired implementation.
- The out-of-the-box Docker setup caused me a small amount of grief, particularly in the fact that only the `/assessment` directory was mapped to my filesystem, so adding packages or adding Django apps (eg: web) required rebuilding the image.  I did at least take the time to add a mapping for the `/api` and `/web` folders so that I could work locally with my editor and see changes reflected in the app without restarting.
- Anything visible from the Web interface is completely un-styled, as the nature of this assessment was presumably backend, so I didn't want to divert time and attention into CSS skills that would be irrelevant (even though I do have them).


## Implementation notes

- As stated, the instructions were rather vague with regard to what this app would be. On one hand it seemed like a service to which third parties would submit batch data, but on the other hand it also implied there might need to be an interface for querying that data.
- Given the uncertainty of how it would be used, I tried to code most of the logic into the models, and put my attention on writing it as an API first.  Those models and the API routes can be found in the `/api` app.
- A secondary app `/web` was created with the intention of just making the other functionality easier to access through a browser.  If I had more free time to waste, I would have built a basic React app to consume the API, rather than making logically duplicated functionality in a secondary Web app.
- I took the time to add unit tests, though I won't pretend that they're comprehensive or complete. If this were production code, there would be more incentive to do that. Also, extensive unit tests are hard to conceive when the expected functionality itself is unclear.  Why test to ensure something working incorrectly?


## Considerations for incomplete Parth 3

I had stubbed in some variables to grab optional filtering inputs in the API (as marked by a TODO in the view) which could then be applied to the model query if the filtering was simply by "key" and "value".  And I think if it weren't for sheer need to spend the rest of my free time doing other things, it wouldn't have been terribly difficult to finish implementing the stubbed code in the API.

Implementing the same thing into the Web interface, however, while not adding terribly much more difficultly, would have definitely eaten much more time due to the need to build HTML to support it, all of which brings me back to the implications of having unclear project requirements.  If this were meant to be only web, or only API, or both, having that spelled out would help. And more importantly, if the browser interface is expected (I saw nothing to indicate yes or no to that) then some manner of mockup and supporting CSS would help to make that possible. Right now, the time that would have been required for CSS to make that work well would have been unreasonable.

Further, there was some mention about these attributes on objects being some mechanism for determining which ones can be attached to _other_ objects, along with some mention of the filtering having specific data types... which all really left a nebulous unanswered issue regarding what this filtering is meant to accomplish and how one might be expected to use it at all.

So this compbination of factors (in addition to time spent on a not-for-pay project) made this a really good stopping point. And again, it can all be discussed during any follow-up interview.

## Final comments

While I've mentioned more than once the balance of time and effort against the not-for-pay nature of a coding assessment, I do want to at least point out that I _did_ actually enjoy a chance to work on something specifically related to python and Django, and to refresh my familiarity with Django in particular after having not used it in a few years. So I don't count this as wasted energy or effort.