import tts
import asyncio
import random

# mas chistes yayo: https://www.3djuegos.com/foros/tema/79735/0/humor-chistes-de-yayo-bastante-sarpados/

chistes_yayo = [
    "Querida preparate porque hoy lo vamos a hacer por la oreja. ¿Por la oreja? me vas a dejar sorda. ¿Cómo te voy a dejar sorda?, Alguna vez te deje muda vieja conchuda y la puta que te parió! Te venís a hacer la santa ahora y te tragaste más pijas que tu vieja y tus 2 hermanas juntas"

    ,
    "El pibe cumple 15 años y no había conocido al padre entonces toma unpoquito de coraje y le pregunta a la madre,  mama,  necesito saber quien es mi papa,   mira hijo, vos sos un bebe de PROBETA,  como bebe de probeta?,  si, probé tantas pijas, conchas y porongas que no se quien puta es tu padre pendejo puto, Forro y tu hermana la mas chica!"

    ,
    "Sube una señora al micro con sus 8 hijitos, uno colgado del saco, otro de las bolsas del supermercado, Al fondo del micro ve un señor casi recostado sobre el asiento con las piernas abiertas y a la señora no le queda mas remedio que sentarse en el pequeño lugar que le había dejado el señor, y la señora le dice muy respetuosamente, señor, si cerrara las piernas habría lugar para uno más, el señor se da vuelta y le responde, y si vos hubieras cerrado la concha habría lugar para todos vieja puta y todos tus pendejos y la re-puta madre que te parió!"

    ,
    "El marido en un momento reflexivo le encara a su señora y le dice, vieja, estuve pensando que si vos te murieras no sabes como te lloraría, a si??? y no me podes mostrar como me llorarías?, primero morite vieja y la re puta madre que te parió y la concha de la recalcada hija de puta de tu hermana!",

    "En un programa de televisión, conducido por una señora tipo Susana Gimenez en donde invita a un señor que decía que había descubierto la verdadera teoría del mal de la vaca loca y el hombre empieza a explicar, bueno, yo he descubierto el mal de la vaca loca, si, y?, y bueno, en primer lugar tenga en cuenta que la vaca se aparea con el toro una vez al año, si, y?, y bueno, en segundo lugar tenga en cuenta que nosotros en el campo ordeñamos a la vaca cuatro veces al día, si, y?, como y? si a vos te manoseo las tetas tres vez al día y te cojo una vez al año como no te vas a volver loca vieja y la re puta madre que te parió!",

    "Llega una señorita muy linda al hotel y el conserje le toma las valijas y la acompaña a la habitación, y cuando están en el ascensor el conserje tiene la mala fortuna de pegarle un codazo en la teta izquierda y para pasar por alto el mal momento improvisa un piropo, señorita, si su corazón es tan tierno como su seno usted sabrá disculparme... y la señorita le responde, bueno, ahora si tu pija es tan dura como tu codo te espero en la habitación 12 así nos echamos una flor de cojida porque tengo la concha ardiente de ganas de tragarme esa flor de chota!",

    "Habían dos amigos charlando de sexo y uno le dice al otro, el otro día hice el 114, y como es el 114?, estaba haciendo la 69 y llego el marido y me metió la 45 en el orto y me rebano el culo y me lo dejo como la cajeta de tu vieja guacho puto y la reconcha de tu hija mas chica!",

    "Resulta que la señorita estaba preocupada porque un pibe la había invitado a salir y se lo comenta a su amiga, mira negra, estoy muy preocupada porque el pibe que me invito a salir me dijo que quería hacer el amor PLATONICO, y eso que es?, y no se, y bueno, por las dudas lavate bien el culo ya veo que te saca una flor de poronga y te taladra el ojete forra de mierda!",

    "Resulta que va la señora al doctor y le manifiesta el problema que tenía, mire doctor, me parece que estoy embarazada. Tengo todos los síntomas del embarazo, no señora, no se preocupe, lo que tiene usted son gases, pero esta seguro doctor??, si señora tranquilícese, Y a los 9 meses el doctor se encuentra a esta señora con un cochecito en donde llevaba a dos nenes mellizos y el doctor le pregunta, señora, esos mellizos son suyos?, si, pero para vos deben ser dos pedos disfrazados de marinerito viejo choto, culo roto y la concha de tu madre!",

    "Había un gallego hablando por la línea erótica y dice, hola, este es un 0-600 erótico?? ,si mi amor... ,y por donde carajo meto la poronga caliente pija hija de puta!",

    "El nene le dice al padre, papa, vos te casaste por civil?, no, me case por vos pendejo pelotudo, Forro pinchado!",

    "La señora se va por 10 días de vacaciones a Cúba y conoce a un negro grandote, musculoso, pijón. Resulta que filo va, filo viene todas las noches hicieron el amor y la señora le pregunta una noche, negro, vos como te llamas?. no, no te voy a decir mi nombre porque te vas a reír. Entonces la última noche, en el momento de la despedida, la señora insiste en saber su nombre, negro, decime tu nombre por favor. no, vos te vas a reír. pero no negro, yo me voy esta noche, que te calienta. bueno, mis padres querían que fuera mujer y en honor a eso me pusieron NIEVE. Y la señora se revolcaba en el piso de la risa y el negro le dice. viste que te ibas a reír de mi nombre, no me rió de tu nombre, me río de la cara que va a poner mi marido cuando le cuente que estuve 10 días en cuba con 25 cms de nieve entre la cajeta y el culo, negro Forro!"]


def contar_chiste(comediante="yayo"):
    if comediante != "yayo":
        raise Exception("No existe el comediante")
    return tts.say(chistes_yayo[random.randint(0, len(chistes_yayo) - 1)])


if __name__ == "__main__":
    asyncio.run(contar_chiste())
