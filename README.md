# Basic translation service Dutch to English

Provides a basic translation service to translate from Dutch to English
based on https://huggingface.co/Helsinki-NLP/opus-mt-nl-en

It uses a MarianMT model
https://huggingface.co/docs/transformers/model_doc/marian to translate
Dutch sentences to English sentences.  A direct translation API is
provided, as well as tooling to enrich data in the triplestore.

By default, this service translates all `@nl` strings it has access to
in the triplestore that are the object of a `dct:description` to english
and stores the translated strings with the same subject and predicate as
`@en` strings.

## Tutorials

### Online string translation

This service provides online translation for user requests through a GET
to `/translate/` with query parameter `source`.

An example call:

    GET /translate?source=wat%20een%20goede%20vertaling

Which may yield a response such as:

    {
      "attributes": {
        "source": "wat een goede vertaling",
        "target": "♪ What a good translation ♪"
      },
      "id": "7905204a-a226-11ed-babd-0242ac1a0004",
      "type": "translations"
    }


### Wiring up this service for direct translation

For direct translation, add this service to your stack and forward
`/translate/` from the dispatcher to this microservice.

In the `docker-compose.yml`

    translations:
      image: madnificent/translation-service

In `config/dispatcher.ex`

    match "/translate/*path" do
      Proxy.forward conn, path, "http://translations/translate/"
    end

Then restart the dispatcher and up your stack:

    docker-compose restart dispatcher; docker-compose up;

You can now make a GET call to `/translate`.  Assuming you are running
on localhost with the identifier published on port 80:

    curl http://localhost/translate/?source=wat%20een%20goede%20vertaling

Feedback should be given on the background.

### Wiring up this service for reactive translation

Reactive services receive updates from the triplestore and process data
based on that state.

For translation with the default configuration, you can wire up the
delta-notifier to inform whenever a change is made to `dct:description`.
This service will translate all available patterns when a change comes
in.  If threading is not increased it will not execute duplicate
calculations.

### Enriching another data model

To enrich another data model, update the functions in the file
`queries.py` and mount the new configuration file.

It is advised to place the new configuration file in your project in
`/config/translate/query.py` and mount it in `/app/` through the
following snippet in your docker-compose.yml:

    translations:
      image: madnificent/translation-service
      volumes:
        - "./config/translations/query.py:/app/query.py"

You can base the contents of `query.py` on the defaults available in
this repository.

## Reference

### Configuration API

`queries.py` can be overwritten with calls to the database.  One query
exists to yield the content to be translated, the next should store the
translated content.  This image is called when a Delta message or
similar appears.

- `queryEnrichableDescriptions`: Yields a list of tuples of which the
  first element is an identifier and the second is the Dutch string to
  translate.
  
- `updateEnrichableDescriptions`: Receives a list of tuples of which the
  first element is the identifier from the previous call and the second
  element is the translated string.

## Discussion

### Why this model

The service's aim is to show how AI algorithms can be integrated in
semantic.works.

The used model is good for testing and validation.  The Marian model is
smaller and some advised use is for fine-tuning experiments and
integration tests.  This matches the goal of the service.
