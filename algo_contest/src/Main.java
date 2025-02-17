import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();

        System.out.println(countWord(line));
    }

    // TODO: реализуйте метод countWord
    private static int countWord(String str) {

        String targetWord = "Rumpelstiltskin";
        Map<Character, Integer> countsMap = new HashMap<>();
        Map<Character, Integer> lettersMap = new HashMap<>();

        for (int i = 0; i < targetWord.length(); i++) {
            char c = Character.toLowerCase(targetWord.charAt(i));
            if (lettersMap.containsKey(c)) {
                if (countsMap.containsKey(c)) {
                    countsMap.put(c, countsMap.get(c) + 1);
                }
                else {
                    countsMap.put(c, 2);
                }
            }
            else {
                lettersMap.put(c, 0);
            }
        }

        for (int i = 0; i < str.length(); i++) {
            char c = Character.toLowerCase(str.charAt(i));
            if(str.charAt(i) != ' ' && lettersMap.containsKey(c)) {
                int currentCount = lettersMap.get(c);
                lettersMap.put(c, currentCount + 1);
            }
        }

        int minCount = Integer.MAX_VALUE;
        for (Map.Entry<Character, Integer> entry : lettersMap.entrySet()) {
            if(countsMap.containsKey(entry.getKey())) {
                int countTimes = countsMap.get(entry.getKey());
                int currentCount = entry.getValue();
                int result = currentCount / countTimes;
                lettersMap.put(entry.getKey(), result);
            }
            if (entry.getValue() < minCount) {
                minCount = entry.getValue();
            }
        }
        return minCount;
    }
}