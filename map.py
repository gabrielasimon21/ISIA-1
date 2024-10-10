import spade
import tkinter as tk
import random

class MapAgent(spade.agent.Agent):
    async def setup(self):
        print("Agente Iniciado!")


GRID_SIZE = 50
CELL_SIZE = 20
fenomenos = ("Terramoto", "Terramoto + Tsunami", "Tsunami", "Incêndio")
fenomeno = random.choice(fenomenos)

# Função que inicia a interface gráfica
def create_gui(root, fenomeno):

    #População em cada célula

    population_data = [[363.0, 303.0, 575.0, 491.0, 156.0, 508.0, 489.0, 166.0, 209.0, 20.0, 142.0, 112.0, 627.0, 324.0, 618.0, 38.0, 536.0, 500.0, 192.0, 417.0, 482.0, 595.0, 133.0, 217.0, 273.0, 61.0, 329.0, 666.0, 162.0, 85.0, 72.0, 22.0, 144.0, 506.0, 632.0, 635.0, 100.0, 546.0, 58.0, 409.0, 361.0, 272.0, 212.0, 485.0, 410.0, 310.0, 361.0, 332.0, 364.0, 370.0], [59.0, 622.0, 422.0, 627.0, 179.0, 305.0, 127.0, 48.0, 657.0, 280.0, 603.0, 596.0, 140.0, 236.0, 467.0, 103.0, 334.0, 676.0, 78.0, 72.0, 425.0, 85.0, 299.0, 62.0, 603.0, 514.0, 522.0, 639.0, 491.0, 448.0, 392.0, 270.0, 598.0, 67.0, 624.0, 81.0, 47.0, 582.0, 435.0, 276.0, 504.0, 91.0, 589.0, 339.0, 200.0, 61.0, 527.0, 521.0, 554.0, 221.0], [543.0, 422.0, 126.0, 661.0, 184.0, 412.0, 25.0, 509.0, 47.0, 323.0, 596.0, 604.0, 107.0, 40.0, 227.0, 65.0, 613.0, 348.0, 46.0, 423.0, 213.0, 325.0, 362.0, 273.0, 682.0, 85.0, 354.0, 605.0, 303.0, 46.0, 617.0, 422.0, 390.0, 558.0, 111.0, 669.0, 377.0, 138.0, 533.0, 679.0, 279.0, 490.0, 429.0, 536.0, 469.0, 671.0, 375.0, 464.0, 449.0, 287.0], [318.0, 566.0, 418.0, 305.0, 249.0, 479.0, 699.0, 144.0, 696.0, 154.0, 51.0, 553.0, 58.0, 270.0, 252.0, 457.0, 66.0, 259.0, 22.0, 616.0, 62.0, 210.0, 468.0, 291.0, 113.0, 39.0, 228.0, 568.0, 417.0, 652.0, 632.0, 24.0, 221.0, 643.0, 104.0, 635.0, 247.0, 94.0, 505.0, 193.0, 504.0, 230.0, 687.0, 337.0, 244.0, 699.0, 296.0, 133.0, 343.0, 385.0], [609.0, 533.0, 91.0, 348.0, 145.0, 20.0, 396.0, 142.0, 181.0, 500.0, 233.0, 306.0, 273.0, 661.0, 534.0, 536.0, 207.0, 191.0, 451.0, 95.0, 439.0, 464.0, 394.0, 81.0, 290.0, 401.0, 411.0, 497.0, 106.0, 459.0, 611.0, 537.0, 266.0, 490.0, 139.0, 210.0, 629.0, 77.0, 339.0, 415.0, 273.0, 85.0, 160.0, 429.0, 602.0, 204.0, 608.0, 236.0, 606.0, 140.0], [657.0, 698.0, 304.0, 259.0, 642.0, 615.0, 261.0, 528.0, 641.0, 78.0, 248.0, 519.0, 559.0, 369.0, 410.0, 219.0, 369.0, 52.0, 70.0, 495.0, 302.0, 518.0, 354.0, 291.0, 599.0, 22.0, 324.0, 356.0, 278.0, 530.0, 324.0, 258.0, 178.0, 319.0, 536.0, 676.0, 301.0, 663.0, 471.0, 290.0, 460.0, 199.0, 411.0, 625.0, 131.0, 691.0, 638.0, 377.0, 180.0, 227.0], [691.0, 79.0, 658.0, 23.0, 493.0, 206.0, 621.0, 538.0, 178.0, 51.0, 459.0, 486.0, 274.0, 544.0, 427.0, 258.0, 524.0, 235.0, 196.0, 341.0, 257.0, 117.0, 537.0, 110.0, 144.0, 158.0, 536.0, 43.0, 192.0, 437.0, 441.0, 324.0, 541.0, 63.0, 310.0, 262.0, 680.0, 576.0, 151.0, 30.0, 569.0, 376.0, 437.0, 524.0, 441.0, 605.0, 366.0, 133.0, 597.0, 140.0], [634.0, 307.0, 519.0, 174.0, 20.0, 403.0, 208.0, 696.0, 479.0, 343.0, 391.0, 341.0, 339.0, 248.0, 125.0, 168.0, 273.0, 232.0, 365.0, 425.0, 357.0, 96.0, 50.0, 668.0, 120.0, 272.0, 497.0, 627.0, 444.0, 302.0, 175.0, 87.0, 444.0, 492.0, 26.0, 95.0, 594.0, 225.0, 95.0, 539.0, 330.0, 50.0, 328.0, 290.0, 231.0, 244.0, 497.0, 204.0, 577.0, 562.0], [571.0, 681.0, 349.0, 327.0, 279.0, 59.0, 608.0, 215.0, 261.0, 498.0, 617.0, 696.0, 357.0, 61.0, 448.0, 528.0, 211.0, 272.0, 43.0, 263.0, 458.0, 397.0, 31.0, 123.0, 154.0, 403.0, 659.0, 89.0, 450.0, 556.0, 209.0, 456.0, 659.0, 443.0, 137.0, 153.0, 317.0, 605.0, 571.0, 624.0, 415.0, 683.0, 306.0, 23.0, 498.0, 378.0, 571.0, 176.0, 431.0, 287.0], [219.0, 242.0, 441.0, 661.0, 135.0, 303.0, 438.0, 168.0, 91.0, 343.0, 276.0, 248.0, 308.0, 125.0, 83.0, 50.0, 314.0, 262.0, 588.0, 184.0, 137.0, 360.0, 554.0, 54.0, 458.0, 42.0, 82.0, 307.0, 49.0, 233.0, 147.0, 452.0, 530.0, 320.0, 588.0, 535.0, 364.0, 574.0, 102.0, 157.0, 94.0, 370.0, 293.0, 183.0, 536.0, 440.0, 51.0, 133.0, 239.0, 266.0], [406.0, 493.0, 344.0, 90.0, 518.0, 523.0, 69.0, 519.0, 142.0, 593.0, 472.0, 490.0, 258.0, 289.0, 240.0, 652.0, 563.0, 557.0, 49.0, 555.0, 70.0, 120.0, 73.0, 195.0, 516.0, 539.0, 356.0, 460.0, 623.0, 234.0, 192.0, 418.0, 220.0, 248.0, 185.0, 444.0, 394.0, 328.0, 645.0, 483.0, 63.0, 543.0, 138.0, 683.0, 531.0, 149.0, 698.0, 434.0, 264.0, 160.0], [73.0, 41.0, 529.0, 178.0, 629.0, 141.0, 552.0, 600.0, 660.0, 693.0, 181.0, 360.0, 517.0, 333.0, 163.0, 347.0, 409.0, 286.0, 95.0, 573.0, 614.0, 47.0, 487.0, 221.0, 253.0, 312.0, 347.0, 318.0, 356.0, 521.0, 326.0, 55.0, 386.0, 670.0, 327.0, 530.0, 339.0, 486.0, 254.0, 365.0, 198.0, 552.0, 338.0, 280.0, 290.0, 636.0, 344.0, 371.0, 316.0, 664.0], [474.0, 41.0, 691.0, 21.0, 389.0, 693.0, 636.0, 357.0, 414.0, 238.0, 294.0, 219.0, 686.0, 595.0, 520.0, 453.0, 521.0, 459.0, 243.0, 144.0, 37.0, 313.0, 354.0, 48.0, 250.0, 294.0, 330.0, 207.0, 656.0, 509.0, 98.0, 541.0, 699.0, 393.0, 280.0, 68.0, 430.0, 586.0, 558.0, 644.0, 572.0, 480.0, 480.0, 141.0, 41.0, 676.0, 138.0, 75.0, 417.0, 221.0], [668.0, 414.0, 362.0, 549.0, 104.0, 340.0, 418.0, 145.0, 602.0, 604.0, 242.0, 603.0, 137.0, 201.0, 412.0, 221.0, 664.0, 692.0, 638.0, 174.0, 472.0, 445.0, 213.0, 302.0, 231.0, 267.0, 165.0, 208.0, 169.0, 372.0, 454.0, 676.0, 47.0, 677.0, 476.0, 46.0, 436.0, 144.0, 526.0, 301.0, 620.0, 121.0, 452.0, 687.0, 138.0, 384.0, 381.0, 24.0, 232.0, 621.0], [592.0, 358.0, 201.0, 700.0, 267.0, 32.0, 508.0, 310.0, 642.0, 518.0, 285.0, 213.0, 686.0, 482.0, 238.0, 568.0, 447.0, 73.0, 344.0, 241.0, 316.0, 110.0, 260.0, 553.0, 369.0, 519.0, 59.0, 126.0, 127.0, 476.0, 80.0, 428.0, 609.0, 180.0, 94.0, 675.0, 289.0, 599.0, 198.0, 623.0, 322.0, 433.0, 432.0, 628.0, 359.0, 187.0, 24.0, 643.0, 335.0, 543.0], [256.0, 524.0, 493.0, 239.0, 358.0, 587.0, 412.0, 566.0, 349.0, 263.0, 677.0, 178.0, 35.0, 639.0, 400.0, 406.0, 348.0, 284.0, 460.0, 175.0, 446.0, 635.0, 485.0, 314.0, 551.0, 552.0, 133.0, 492.0, 541.0, 260.0, 662.0, 129.0, 464.0, 189.0, 128.0, 283.0, 271.0, 145.0, 522.0, 287.0, 552.0, 470.0, 304.0, 46.0, 341.0, 568.0, 193.0, 162.0, 354.0, 246.0], [405.0, 539.0, 369.0, 206.0, 650.0, 519.0, 54.0, 109.0, 372.0, 628.0, 460.0, 653.0, 602.0, 293.0, 595.0, 156.0, 314.0, 90.0, 422.0, 70.0, 673.0, 445.0, 47.0, 248.0, 45.0, 175.0, 34.0, 268.0, 323.0, 522.0, 345.0, 72.0, 50.0, 525.0, 182.0, 332.0, 394.0, 538.0, 383.0, 130.0, 409.0, 460.0, 545.0, 401.0, 140.0, 194.0, 638.0, 446.0, 206.0, 309.0], [466.0, 106.0, 568.0, 421.0, 447.0, 207.0, 445.0, 632.0, 575.0, 246.0, 60.0, 89.0, 165.0, 368.0, 462.0, 365.0, 548.0, 220.0, 428.0, 63.0, 364.0, 443.0, 613.0, 556.0, 270.0, 586.0, 630.0, 192.0, 282.0, 331.0, 579.0, 213.0, 506.0, 666.0, 431.0, 233.0, 607.0, 381.0, 349.0, 675.0, 358.0, 181.0, 202.0, 564.0, 652.0, 179.0, 36.0, 579.0, 264.0, 297.0], [199.0, 71.0, 168.0, 699.0, 647.0, 687.0, 108.0, 94.0, 268.0, 629.0, 664.0, 309.0, 275.0, 417.0, 501.0, 673.0, 376.0, 205.0, 408.0, 353.0, 530.0, 306.0, 272.0, 118.0, 176.0, 222.0, 627.0, 284.0, 134.0, 686.0, 405.0, 421.0, 213.0, 59.0, 69.0, 115.0, 420.0, 501.0, 264.0, 213.0, 96.0, 371.0, 628.0, 691.0, 678.0, 210.0, 285.0, 386.0, 570.0, 683.0], [652.0, 603.0, 397.0, 513.0, 75.0, 245.0, 341.0, 654.0, 318.0, 109.0, 525.0, 270.0, 307.0, 576.0, 179.0, 33.0, 378.0, 403.0, 328.0, 303.0, 453.0, 472.0, 572.0, 604.0, 103.0, 561.0, 371.0, 247.0, 454.0, 111.0, 280.0, 612.0, 430.0, 95.0, 561.0, 611.0, 679.0, 85.0, 51.0, 119.0, 325.0, 162.0, 607.0, 158.0, 669.0, 344.0, 530.0, 218.0, 436.0, 627.0], [686.0, 121.0, 178.0, 195.0, 220.0, 440.0, 582.0, 120.0, 683.0, 647.0, 399.0, 111.0, 356.0, 193.0, 593.0, 446.0, 332.0, 223.0, 105.0, 200.0, 209.0, 452.0, 56.0, 31.0, 343.0, 35.0, 380.0, 230.0, 312.0, 176.0, 479.0, 451.0, 441.0, 182.0, 73.0, 214.0, 670.0, 166.0, 680.0, 307.0, 424.0, 427.0, 201.0, 441.0, 314.0, 442.0, 173.0, 144.0, 344.0, 408.0], [375.0, 560.0, 183.0, 245.0, 217.0, 209.0, 517.0, 602.0, 577.0, 631.0, 572.0, 475.0, 532.0, 358.0, 325.0, 236.0, 246.0, 330.0, 429.0, 474.0, 532.0, 613.0, 320.0, 647.0, 163.0, 341.0, 633.0, 698.0, 58.0, 254.0, 76.0, 253.0, 546.0, 362.0, 165.0, 22.0, 199.0, 567.0, 440.0, 431.0, 192.0, 682.0, 619.0, 477.0, 241.0, 563.0, 306.0, 23.0, 644.0, 262.0], [452.0, 173.0, 478.0, 465.0, 68.0, 540.0, 71.0, 552.0, 566.0, 504.0, 144.0, 197.0, 256.0, 390.0, 627.0, 114.0, 29.0, 695.0, 90.0, 392.0, 66.0, 158.0, 153.0, 376.0, 445.0, 170.0, 56.0, 147.0, 633.0, 293.0, 276.0, 552.0, 516.0, 424.0, 473.0, 331.0, 680.0, 215.0, 297.0, 325.0, 259.0, 679.0, 699.0, 252.0, 393.0, 675.0, 512.0, 497.0, 139.0, 74.0], [59.0, 507.0, 93.0, 49.0, 444.0, 208.0, 127.0, 199.0, 197.0, 130.0, 623.0, 464.0, 107.0, 445.0, 66.0, 674.0, 513.0, 629.0, 205.0, 605.0, 86.0, 171.0, 337.0, 623.0, 55.0, 274.0, 442.0, 36.0, 485.0, 127.0, 269.0, 546.0, 683.0, 218.0, 239.0, 620.0, 41.0, 170.0, 610.0, 501.0, 566.0, 22.0, 451.0, 203.0, 90.0, 689.0, 210.0, 51.0, 325.0, 505.0], [142.0, 225.0, 175.0, 169.0, 253.0, 377.0, 498.0, 434.0, 412.0, 342.0, 391.0, 654.0, 440.0, 35.0, 318.0, 392.0, 584.0, 663.0, 230.0, 421.0, 369.0, 502.0, 280.0, 442.0, 504.0, 417.0, 524.0, 126.0, 478.0, 39.0, 462.0, 548.0, 672.0, 316.0, 589.0, 413.0, 674.0, 334.0, 459.0, 618.0, 381.0, 224.0, 699.0, 264.0, 145.0, 285.0, 281.0, 619.0, 92.0, 316.0], [155.0, 182.0, 391.0, 177.0, 460.0, 495.0, 643.0, 302.0, 383.0, 477.0, 517.0, 189.0, 600.0, 430.0, 98.0, 238.0, 657.0, 137.0, 682.0, 693.0, 281.0, 222.0, 512.0, 316.0, 35.0, 291.0, 88.0, 251.0, 294.0, 694.0, 268.0, 377.0, 250.0, 362.0, 181.0, 175.0, 105.0, 213.0, 169.0, 387.0, 196.0, 605.0, 421.0, 558.0, 152.0, 614.0, 179.0, 26.0, 287.0, 73.0], [228.0, 121.0, 630.0, 409.0, 330.0, 397.0, 291.0, 30.0, 264.0, 660.0, 455.0, 287.0, 246.0, 509.0, 72.0, 497.0, 455.0, 281.0, 211.0, 68.0, 587.0, 283.0, 629.0, 81.0, 80.0, 293.0, 386.0, 394.0, 568.0, 77.0, 206.0, 67.0, 222.0, 696.0, 363.0, 131.0, 689.0, 583.0, 243.0, 157.0, 95.0, 658.0, 308.0, 552.0, 244.0, 25.0, 396.0, 315.0, 279.0, 685.0], [398.0, 254.0, 569.0, 391.0, 447.0, 619.0, 576.0, 598.0, 579.0, 466.0, 399.0, 98.0, 159.0, 205.0, 588.0, 469.0, 671.0, 323.0, 342.0, 541.0, 528.0, 584.0, 399.0, 466.0, 594.0, 460.0, 594.0, 142.0, 286.0, 255.0, 95.0, 311.0, 143.0, 372.0, 40.0, 699.0, 94.0, 628.0, 535.0, 290.0, 628.0, 623.0, 602.0, 99.0, 409.0, 561.0, 204.0, 450.0, 83.0, 427.0], [551.0, 391.0, 57.0, 612.0, 286.0, 337.0, 612.0, 391.0, 536.0, 674.0, 379.0, 178.0, 689.0, 119.0, 164.0, 318.0, 695.0, 311.0, 272.0, 503.0, 508.0, 172.0, 312.0, 489.0, 432.0, 507.0, 525.0, 459.0, 476.0, 102.0, 475.0, 548.0, 367.0, 446.0, 447.0, 472.0, 32.0, 101.0, 257.0, 639.0, 478.0, 245.0, 470.0, 271.0, 510.0, 191.0, 95.0, 620.0, 600.0, 98.0], [405.0, 410.0, 546.0, 394.0, 527.0, 653.0, 696.0, 210.0, 260.0, 80.0, 375.0, 52.0, 76.0, 679.0, 303.0, 324.0, 310.0, 389.0, 152.0, 46.0, 296.0, 106.0, 118.0, 116.0, 46.0, 366.0, 586.0, 635.0, 189.0, 256.0, 463.0, 455.0, 627.0, 334.0, 653.0, 570.0, 190.0, 540.0, 377.0, 573.0, 405.0, 348.0, 496.0, 46.0, 186.0, 331.0, 125.0, 588.0, 59.0, 652.0], [199.0, 304.0, 67.0, 365.0, 643.0, 29.0, 700.0, 589.0, 603.0, 176.0, 407.0, 474.0, 448.0, 311.0, 53.0, 482.0, 171.0, 28.0, 225.0, 517.0, 479.0, 655.0, 541.0, 143.0, 564.0, 164.0, 613.0, 495.0, 587.0, 203.0, 543.0, 315.0, 646.0, 401.0, 217.0, 364.0, 136.0, 142.0, 613.0, 395.0, 115.0, 322.0, 650.0, 660.0, 128.0, 421.0, 92.0, 252.0, 198.0, 144.0], [598.0, 568.0, 560.0, 55.0, 449.0, 43.0, 465.0, 410.0, 489.0, 469.0, 440.0, 554.0, 639.0, 260.0, 351.0, 332.0, 56.0, 422.0, 568.0, 486.0, 223.0, 331.0, 454.0, 67.0, 91.0, 627.0, 513.0, 453.0, 108.0, 220.0, 497.0, 84.0, 327.0, 645.0, 281.0, 35.0, 239.0, 445.0, 343.0, 356.0, 687.0, 456.0, 599.0, 329.0, 237.0, 652.0, 72.0, 487.0, 695.0, 659.0], [387.0, 315.0, 444.0, 282.0, 320.0, 324.0, 652.0, 642.0, 683.0, 262.0, 153.0, 258.0, 221.0, 51.0, 563.0, 496.0, 615.0, 586.0, 55.0, 178.0, 42.0, 402.0, 173.0, 32.0, 318.0, 595.0, 533.0, 73.0, 429.0, 67.0, 526.0, 452.0, 282.0, 177.0, 627.0, 338.0, 280.0, 251.0, 636.0, 142.0, 449.0, 540.0, 381.0, 591.0, 548.0, 684.0, 543.0, 612.0, 538.0, 526.0], [68.0, 126.0, 656.0, 602.0, 623.0, 130.0, 297.0, 468.0, 43.0, 641.0, 429.0, 519.0, 96.0, 172.0, 654.0, 515.0, 77.0, 438.0, 521.0, 550.0, 550.0, 504.0, 29.0, 609.0, 425.0, 628.0, 275.0, 311.0, 431.0, 252.0, 53.0, 639.0, 297.0, 142.0, 235.0, 215.0, 527.0, 117.0, 553.0, 459.0, 665.0, 561.0, 545.0, 392.0, 58.0, 457.0, 511.0, 618.0, 45.0, 122.0], [132.0, 598.0, 58.0, 431.0, 67.0, 677.0, 290.0, 156.0, 638.0, 174.0, 570.0, 46.0, 143.0, 32.0, 140.0, 314.0, 347.0, 652.0, 196.0, 563.0, 279.0, 331.0, 336.0, 655.0, 617.0, 549.0, 638.0, 438.0, 479.0, 498.0, 414.0, 179.0, 525.0, 653.0, 555.0, 129.0, 383.0, 462.0, 90.0, 232.0, 656.0, 359.0, 193.0, 282.0, 332.0, 486.0, 283.0, 617.0, 517.0, 140.0], [545.0, 649.0, 638.0, 186.0, 29.0, 89.0, 568.0, 388.0, 676.0, 547.0, 598.0, 270.0, 226.0, 418.0, 492.0, 445.0, 698.0, 431.0, 509.0, 41.0, 673.0, 101.0, 170.0, 81.0, 495.0, 144.0, 544.0, 417.0, 432.0, 257.0, 688.0, 369.0, 652.0, 695.0, 498.0, 303.0, 660.0, 199.0, 358.0, 186.0, 57.0, 356.0, 349.0, 354.0, 290.0, 57.0, 360.0, 108.0, 600.0, 581.0], [283.0, 600.0, 204.0, 120.0, 546.0, 43.0, 298.0, 521.0, 125.0, 315.0, 87.0, 343.0, 464.0, 687.0, 491.0, 575.0, 690.0, 22.0, 40.0, 321.0, 170.0, 164.0, 536.0, 641.0, 169.0, 654.0, 197.0, 96.0, 340.0, 267.0, 378.0, 382.0, 542.0, 159.0, 389.0, 173.0, 391.0, 234.0, 471.0, 91.0, 445.0, 86.0, 326.0, 410.0, 602.0, 473.0, 176.0, 628.0, 480.0, 288.0], [164.0, 530.0, 357.0, 608.0, 338.0, 677.0, 573.0, 688.0, 31.0, 278.0, 104.0, 493.0, 33.0, 167.0, 330.0, 575.0, 189.0, 341.0, 364.0, 587.0, 143.0, 222.0, 154.0, 360.0, 123.0, 210.0, 490.0, 661.0, 214.0, 580.0, 419.0, 119.0, 619.0, 438.0, 464.0, 296.0, 558.0, 261.0, 112.0, 403.0, 275.0, 86.0, 124.0, 205.0, 636.0, 91.0, 283.0, 22.0, 215.0, 116.0], [683.0, 400.0, 564.0, 314.0, 162.0, 238.0, 306.0, 158.0, 231.0, 361.0, 485.0, 267.0, 545.0, 213.0, 199.0, 418.0, 410.0, 422.0, 492.0, 567.0, 45.0, 414.0, 94.0, 20.0, 84.0, 85.0, 464.0, 296.0, 441.0, 423.0, 143.0, 477.0, 304.0, 637.0, 690.0, 120.0, 278.0, 434.0, 32.0, 125.0, 693.0, 438.0, 396.0, 410.0, 634.0, 422.0, 634.0, 147.0, 667.0, 330.0], [90.0, 615.0, 196.0, 361.0, 151.0, 245.0, 437.0, 101.0, 134.0, 307.0, 585.0, 334.0, 470.0, 193.0, 600.0, 103.0, 529.0, 26.0, 183.0, 363.0, 652.0, 338.0, 128.0, 186.0, 245.0, 649.0, 226.0, 83.0, 427.0, 116.0, 526.0, 23.0, 672.0, 126.0, 347.0, 570.0, 542.0, 607.0, 688.0, 626.0, 410.0, 296.0, 523.0, 229.0, 399.0, 278.0, 481.0, 29.0, 533.0, 184.0], [510.0, 378.0, 456.0, 351.0, 227.0, 610.0, 66.0, 671.0, 218.0, 61.0, 358.0, 542.0, 73.0, 480.0, 410.0, 216.0, 369.0, 493.0, 103.0, 164.0, 127.0, 130.0, 570.0, 282.0, 576.0, 158.0, 106.0, 56.0, 455.0, 353.0, 213.0, 329.0, 396.0, 481.0, 694.0, 85.0, 92.0, 430.0, 131.0, 443.0, 409.0, 528.0, 467.0, 195.0, 400.0, 319.0, 600.0, 499.0, 680.0, 452.0], [85.0, 540.0, 444.0, 150.0, 20.0, 533.0, 228.0, 63.0, 578.0, 453.0, 511.0, 618.0, 530.0, 391.0, 352.0, 85.0, 567.0, 267.0, 278.0, 632.0, 357.0, 653.0, 212.0, 120.0, 260.0, 424.0, 215.0, 579.0, 371.0, 162.0, 457.0, 544.0, 26.0, 580.0, 522.0, 72.0, 273.0, 443.0, 500.0, 373.0, 101.0, 419.0, 192.0, 517.0, 189.0, 587.0, 218.0, 382.0, 453.0, 92.0], [698.0, 403.0, 429.0, 109.0, 530.0, 455.0, 447.0, 286.0, 517.0, 370.0, 590.0, 599.0, 226.0, 291.0, 679.0, 298.0, 36.0, 481.0, 460.0, 627.0, 650.0, 25.0, 512.0, 115.0, 229.0, 278.0, 465.0, 209.0, 449.0, 431.0, 269.0, 389.0, 395.0, 136.0, 545.0, 464.0, 664.0, 385.0, 556.0, 261.0, 527.0, 242.0, 227.0, 608.0, 320.0, 658.0, 514.0, 283.0, 233.0, 435.0], [589.0, 486.0, 486.0, 168.0, 99.0, 465.0, 51.0, 420.0, 571.0, 136.0, 189.0, 636.0, 580.0, 677.0, 665.0, 425.0, 63.0, 193.0, 137.0, 249.0, 158.0, 425.0, 434.0, 36.0, 457.0, 326.0, 29.0, 315.0, 192.0, 402.0, 318.0, 140.0, 224.0, 32.0, 124.0, 258.0, 657.0, 635.0, 157.0, 356.0, 78.0, 40.0, 398.0, 693.0, 494.0, 534.0, 678.0, 614.0, 641.0, 642.0], [358.0, 591.0, 559.0, 423.0, 481.0, 276.0, 150.0, 124.0, 369.0, 498.0, 423.0, 400.0, 596.0, 351.0, 91.0, 507.0, 230.0, 459.0, 30.0, 434.0, 259.0, 297.0, 664.0, 279.0, 323.0, 198.0, 142.0, 327.0, 369.0, 329.0, 615.0, 301.0, 257.0, 342.0, 584.0, 70.0, 479.0, 422.0, 304.0, 191.0, 341.0, 198.0, 24.0, 500.0, 495.0, 302.0, 186.0, 627.0, 456.0, 332.0], [546.0, 115.0, 346.0, 382.0, 526.0, 150.0, 597.0, 395.0, 619.0, 176.0, 256.0, 387.0, 340.0, 175.0, 620.0, 259.0, 560.0, 183.0, 436.0, 658.0, 211.0, 123.0, 593.0, 273.0, 290.0, 256.0, 90.0, 455.0, 551.0, 36.0, 238.0, 677.0, 137.0, 561.0, 687.0, 609.0, 162.0, 614.0, 363.0, 35.0, 112.0, 380.0, 336.0, 461.0, 474.0, 327.0, 312.0, 123.0, 518.0, 537.0], [204.0, 392.0, 552.0, 352.0, 379.0, 89.0, 123.0, 46.0, 295.0, 527.0, 334.0, 41.0, 418.0, 671.0, 581.0, 361.0, 410.0, 351.0, 348.0, 449.0, 541.0, 570.0, 101.0, 545.0, 374.0, 501.0, 36.0, 644.0, 136.0, 557.0, 449.0, 0, 0, 0, 0, 0, 0, 0, 158.0, 431.0, 512.0, 317.0, 171.0, 263.0, 628.0, 495.0, 97.0, 195.0, 536.0, 198.0], [696.0, 634.0, 40.0, 409.0, 456.0, 516.0, 534.0, 81.0, 656.0, 189.0, 600.0, 692.0, 163.0, 644.0, 523.0, 320.0, 167.0, 154.0, 499.0, 519.0, 310.0, 373.0, 339.0, 408.0, 395.0, 458.0, 307.0, 373.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128.0, 253.0, 312.0, 97.0, 195.0, 29.0, 35.0, 354.0, 468.0, 605.0, 197.0], [662.0, 63.0, 305.0, 536.0, 117.0, 252.0, 113.0, 510.0, 50.0, 189.0, 206.0, 320.0, 317.0, 522.0, 311.0, 583.0, 589.0, 319.0, 632.0, 59.0, 56.0, 437.0, 365.0, 461.0, 330.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 561.0, 157.0, 447.0, 434.0, 358.0, 465.0, 504.0, 671.0, 69.0, 608.0], [49.0, 342.0, 88.0, 231.0, 380.0, 264.0, 431.0, 381.0, 266.0, 253.0, 162.0, 114.0, 525.0, 352.0, 677.0, 636.0, 419.0, 623.0, 190.0, 160.0, 20.0, 249.0, 404.0, 101.0, 628.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 464.0, 691.0, 186.0, 314.0, 516.0, 202.0, 451.0]]
    n_mortos = 0
    n_feridos = 0
    #Desenho Mapa

    root.title(f"Mapa Cidade: {fenomeno}")
    root2.title("Dados de destruição")

    frame = tk.Frame(root)
    frame.grid(column=0, row=0, padx=10, pady=10)

    canvas = tk.Canvas(frame, width= 900, height=600)
    canvas.grid(row=0, column=0)

    hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    hbar.grid(row=1, column=0, sticky=tk.EW)
    vbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    vbar.grid(row=0, column=1, sticky=tk.NS)

    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.config(scrollregion=(0, 0, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

    def draw_points(canvas, points):
        for key, value in points.items():
            x_cell, y_cell = key
            color = value
            x = x_cell * CELL_SIZE
            y = y_cell * CELL_SIZE
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)

    points = {(44, 4): 'black', (45, 44): 'green', (18, 43): 'magenta', (21, 8): 'magenta', (31, 7): 'magenta', (32, 41): 'magenta', (33, 46): 'magenta', (9, 12): 'red', (44, 22): 'red', (23, 37): 'red', (46, 47): 'red', (3, 41): 'red', (1, 14): 'blue', (5, 40): 'blue', (7, 15): 'blue', (4, 6): 'blue', (17, 36): 'blue', (26, 34): 'blue', (37, 28): 'blue', (41, 12): 'blue'}

    def get_color(population):
        if population == 0:
            return 'light blue'
        elif population < 100:
            return "#d3d3d3"
        elif population < 500:
            return "#a9a9a9"
        else:
            return "#696969"

    legend_colors_earthquake = [0] * 30
    legend_intensity_earthquake = [0] * 30
    legend_colors_tsunami = [0] * 30
    legend_intensity_tsunami = [0] * 30
    legend_colors_fire = [0] * 30
    legend_intensity_fire = [0] * 30

    #Terramoto

    def calculate_color_earthquake (gravity, distance, legend_colors_earthquake, legend_intensity_earthquake):

        max_intensity = 100
        min_intensity = 255

        intensity = max_intensity - int((distance / gravity) * (max_intensity - min_intensity))

        color = f'#{intensity:02x}0000'

        if color not in legend_colors_earthquake:
            legend_intensity_earthquake.append(intensity)
            legend_colors_earthquake.append(color)

        return color

    if (fenomeno == "Terramoto"):
        epicenter_x = random.randint(10, 40)
        epicenter_y = random.randint(10, 40)
        gravity = random.randint(3, 10)
        affected_services_earthquake = [[0 for _ in range(50)] for _ in range(50)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                distance = max(abs(epicenter_x - i), abs(epicenter_y - j))
                if distance <= gravity:
                    if population_data [i][j] != 0:
                        color = calculate_color_earthquake(gravity, distance, legend_colors_earthquake, legend_intensity_earthquake)

                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_earthquake.append(point)
                else:
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

    def calculate_color_tsunami(distance_sea, distance_tsunami, legend_colors_tsunami, legend_intensity_tsunami):
        max_intensity = 255
        min_intensity = 100

        intensity = min_intensity + int((distance_sea / distance_tsunami) * (max_intensity - min_intensity))

        intensity = max(min_intensity, min(max_intensity, intensity))

        color = f'#0000{intensity:02x}'

        if color not in legend_colors_tsunami:
            legend_intensity_tsunami.append(intensity)
            legend_colors_tsunami.append(color)

        return color

    def calculate_distance_sea (i, j):
        sea_points = [(46, 31), (46, 32), (46, 33), (46, 34), (46, 35), (46, 36), (46, 37), (47, 28), (47, 29), (47, 30), (47, 31),
         (47, 32), (47, 33), (47, 34), (47, 35), (47, 36), (47, 37), (47, 38), (48, 25), (48, 26), (48, 27), (48, 28),
         (48, 29), (48, 30), (48, 31), (48, 32), (48, 33), (48, 34), (48, 35), (48, 36), (48, 37), (48, 38), (48, 39),
         (49, 25), (49, 26), (49, 27), (49, 28), (49, 29), (49, 30), (49, 31), (49, 32), (49, 33), (49, 34), (49, 35),
         (49, 36), (49, 37), (49, 38), (49, 39), (49, 40), (49, 41), (49, 42)]

        min_distance = 50
        for point in sea_points:
            distance = max(abs(point[0] - i), abs(point[1] - j))
            if distance < min_distance:
                min_distance = distance
        return min_distance



    if (fenomeno == "Tsunami"):
        distance_tsunami = random.randint(5, 15)
        affected_services_tsunami = [[0 for _ in range(50)] for _ in range(50)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                distance_sea = calculate_distance_sea (i, j)
                if distance_sea <= distance_tsunami and distance_sea != 0:
                    if population_data [i][j] != 0:
                        color = calculate_color_tsunami(distance_sea, distance_tsunami, legend_colors_tsunami, legend_intensity_tsunami)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_tsunami.append(point)
                else:
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE, outline="black", fill=color)


    if (fenomeno == "Terramoto + Tsunami"):
        epicenter_x = random.randint(10, 40)
        epicenter_y = random.randint(10, 40)
        gravity = random.randint(3, 10)
        distance_tsunami = random.randint(5, 15)
        affected_services_earthquake = [[0 for _ in range(50)] for _ in range(50)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                distance = max(abs(epicenter_x - i), abs(epicenter_y - j))
                distance_sea = calculate_distance_sea(i, j)
                if distance <= gravity:
                    if population_data [i][j] != 0:
                        color = calculate_color_earthquake(gravity, distance, legend_colors_earthquake, legend_intensity_earthquake)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_earthquake.append(point)
                elif distance_sea <= distance_tsunami and distance_sea != 0:
                    if population_data [i][j] != 0:
                        color = calculate_color_tsunami(distance_sea, distance_tsunami, legend_colors_tsunami, legend_intensity_tsunami)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_earthquake.append(point)
                else:
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

    def calculate_color_fire ():
        intensities = (100, 160, 130)
        intensity = random.sample(intensities, 1)[0]

        if intensity == 160:
            color = 'yellow'
        elif intensity == 130:
            color = 'orange'
        else:
            color = 'red'

        return color

    if (fenomeno == "Incêndio"):
        area = random.randint(150, 500)
        points_fire = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
        legend_intensity_fire.append(100)
        legend_intensity_fire.append(130)
        legend_intensity_fire.append(160)
        legend_colors_fire.append('red')
        legend_colors_fire.append('orange')
        legend_colors_fire.append('yellow')
        affected_services_fire = [[0 for _ in range(50)] for _ in range(50)]
        while len(points_fire) < area:
            x, y = random.choice(points_fire)
            new_point = (x + random.choice([-1, 1, 0, 0]), y + random.choice([0, 0, -1, 1]))
            if new_point not in points_fire and 0 <= new_point[0] < GRID_SIZE and 0 <= new_point[1] < GRID_SIZE:
                points_fire.append(new_point)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) in points_fire and population_data[i][j] != 0:
                    if population_data [i][j] != 0:
                        color = calculate_color_fire ()
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_fire.append(point)
                else:
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
    #Legendas do Mapa

    draw_points (canvas, points)
    legend_frame = tk.Frame(root)
    legend_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.N)

    tk.Label(legend_frame, text="População/Mar:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Menos de 100", bg="#d3d3d3", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="100 a 499", bg="#a9a9a9", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="500 ou mais", bg="#696969", fg="white", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Mar", bg="light blue", fg="black", width=20).pack(anchor=tk.W)

    descricoes = ["Nº de mortos: ", "Nº de feridos: ", "Nº esquadras destruídas: ", "Nº de quartéis destruídos: ", "Nº de hospitais destruídos: ", "Nº de bases destruídas: "]

    if fenomeno == "Terramoto" or fenomeno == "Terramoto + Tsunami":
        tk.Label(legend_frame, text="Grau de destruição Terramoto:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(legend_colors_earthquake)):
            intensity = legend_intensity_earthquake [i]
            color = legend_colors_earthquake [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)
        dados = [0] * 6
        n_policias = 0
        n_bombeiros = 0
        n_hospitais = 0
        n_bases = 0
        dados [0] = int(n_mortos)
        dados [1] = int(n_feridos)
        for point in affected_services_earthquake:
            i, j = point[0], point[1]
            if (i, j) in points:
                color = points[(i, j)]
                if color == 'blue':
                    n_policias += 1
                elif color == 'red':
                    n_bombeiros += 1
                elif color == 'magenta':
                    n_hospitais += 1
                else:
                    n_bases += 1
        dados [2] = n_policias
        dados [3] = n_bombeiros
        dados [4] = n_hospitais
        dados [5] = n_bases
        for i in range (len(descricoes)):
            descricao = descricoes [i]
            valor = dados [i]
            label_descricao = tk.Label(root2, text=descricao)
            label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            label_valor = tk.Label(root2, text=valor)
            label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    if fenomeno == "Tsunami" or fenomeno == "Terramoto + Tsunami":
        tk.Label(legend_frame, text="Grau de destruição Tsunami:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(legend_colors_tsunami)):
            intensity = legend_intensity_tsunami [i]
            color = legend_colors_tsunami [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)
    if fenomeno == 'Tsunami':
        dados = [0] * 6
        n_policias = 0
        n_bombeiros = 0
        n_hospitais = 0
        n_bases = 0
        dados [0] = int(n_mortos)
        dados [1] = int(n_feridos)
        for point in affected_services_tsunami:
            i, j = point[0], point[1]
            if (i, j) in points:
                color = points[(i, j)]
                if color == 'blue':
                    n_policias += 1
                elif color == 'red':
                    n_bombeiros += 1
                elif color == 'magenta':
                    n_hospitais += 1
                else:
                    n_bases += 1
        dados [2] = n_policias
        dados [3] = n_bombeiros
        dados [4] = n_hospitais
        dados [5] = n_bases
        for i in range (len(descricoes)):
            descricao = descricoes [i]
            valor = dados [i]
            label_descricao = tk.Label(root2, text=descricao)
            label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            label_valor = tk.Label(root2, text=valor)
            label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    if fenomeno == "Incêndio":
        tk.Label(legend_frame, text="Grau de destruição Incêndio:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(legend_colors_fire)):
            intensity = legend_intensity_fire [i]
            color = legend_colors_fire [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)
        dados = [0] * 6
        n_policias = 0
        n_bombeiros = 0
        n_hospitais = 0
        n_bases = 0
        dados [0] = int(n_mortos)
        dados [1] = int(n_feridos)
        for point in affected_services_fire:
            i, j = point[0], point[1]
            if (i, j) in points:
                color = points[(i, j)]
                if color == 'blue':
                    n_policias += 1
                elif color == 'red':
                    n_bombeiros += 1
                elif color == 'magenta':
                    n_hospitais += 1
                else:
                    n_bases += 1
        dados [2] = n_policias
        dados [3] = n_bombeiros
        dados [4] = n_hospitais
        dados [5] = n_bases
        for i in range (len(descricoes)):
            descricao = descricoes [i]
            valor = dados [i]
            label_descricao = tk.Label(root2, text=descricao)
            label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            label_valor = tk.Label(root2, text=valor)
            label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    colors = ('red', 'blue', 'magenta', 'black', 'green')
    color_legend = ("Bombeiros", "Polícia", "Hospital", "Exército", "Força Aérea")
    tk.Label(legend_frame, text="Serviços:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    for i in range (5):
        color = colors[i]
        subtitle = color_legend[i]
        item_frame = tk.Frame(legend_frame, bg="#696969")
        item_frame.pack(side=tk.TOP, anchor="w")
        label = tk.Label(item_frame, text=subtitle, bg="#696969", fg="white")
        label.pack(side=tk.RIGHT)
        canvas = tk.Canvas(item_frame, width=20, height=20, bg="#696969", highlightthickness=0)
        canvas.create_oval(5, 5, 15, 15, fill=color)
        canvas.pack(side=tk.RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    root2 = tk.Tk()
    create_gui(root, fenomeno)
    root.mainloop()

