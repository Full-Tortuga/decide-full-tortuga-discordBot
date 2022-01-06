# discordBot
Votitos es un bot de Discord desarrollado para el módulo de Visualización de Decide. Está pensado para ofrecer información sobre las distintas votaciones así como su resultado. 
Cuenta con distintos comandos. 

- El comando !hi: Suponemos que un nuevo usuario lo primero que hará será saludar al bot. Este comando te ofrece una breve explicación de la funcionalidad del bot y te indica que con !helpcommands puedes ver todos los comandos disponibles.

- !helpcommands: Como hemos dicho previamente, usando este comando, el bot te devuelve una lista de los comandos que puedes utilizar.

- !details: Es un comando que requiere dos parámetros, tipo de votación y número de votación. Una vez solicitas los detalles de una votación correctamente el bot te devuelve el nombre de esta, el id y la descripción.

- !results: Este comando, al igual que el anterior necesita el tipo y el número de votación. Devuelve los detalles de la votación, así como sus opciones y cuántos votos ha obtenido cada una. Si la votación no está cerrada, el bot te avisará que no puedes ver los resultados todavía.

- !graphs: También le hace falta tener el tipo de votación y el número. Cuando lo solicitas, te manda un mensaje de que te las mandará pronto, y acto seguido te las envía. Si la votación no tiene gráficas generadas o no se encuentra la votación, te manda un mensaje diciéndote que no se pudo encontrar.

- !types: Muestra los tipos de votación disponibles que hay para que la persona que quiera pasarlo como parámetro sepa cuáles hay y cómo se escribirían.
